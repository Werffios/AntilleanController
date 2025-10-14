import logging
from typing import List, Optional
from passlib.context import CryptContext
from app.services.database_service import DatabaseService
from app.models.user_models import UserCreate, UserUpdate, UserResponse

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self):
        self.db_service = DatabaseService()

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def create_user(self, user: UserCreate) -> UserResponse:
        try:
            await self.db_service.connect()
            hashed_password = self.get_password_hash(user.password)

            query = """
                    INSERT INTO users (name, email, password, created_at, updated_at)
                    VALUES (%s, %s, %s, NOW(), NOW()) \
                    """
            params = (user.name, user.email, hashed_password)

            result = await self.db_service.execute(query, params)
            new_user_id = result[0]['last_insert_id']

            created_user = await self.get_user_by_id(new_user_id)
            if created_user:
                return created_user

            raise ValueError("User creation failed")
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            raise

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT id, name, email, email_verified_at, created_at, updated_at FROM users WHERE id = %s"
            result = await self.db_service.execute(query, (user_id,))
            if result:
                return UserResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving user: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    # Todo: Aquí irían los métodos get_all_users, update_user y delete_user, siguiendo el mismo patrón que en los otros servicios.