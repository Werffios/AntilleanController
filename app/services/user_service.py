import logging
from typing import Optional
from passlib.context import CryptContext
from app.services.database_service import DatabaseService
from app.models.user_models import UserCreate, UserResponse
from app.models.auth_models import RegisterRequest, LoginRequest
from app.security.crypto_utils import decrypt_text

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self):
        self.db_service = DatabaseService()

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

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
        finally:
            try:
                await self.db_service.disconnect()
            except Exception:
                pass

    async def register_from_encrypted(self, req: RegisterRequest) -> UserResponse:
        """Registra un usuario recibiendo email y password encriptados (Fernet)."""
        try:
            await self.db_service.connect()
            email = decrypt_text(req.email_encrypted).strip().lower()
            password = decrypt_text(req.password_encrypted)
            # Verificar si existe
            existing = await self.get_user_by_email(email, _already_connected=True)
            if existing:
                raise ValueError("El email ya está registrado")
            hashed_password = self.get_password_hash(password)
            query = (
                "INSERT INTO users (name, email, password, created_at, updated_at) "
                "VALUES (%s, %s, %s, NOW(), NOW())"
            )
            params = (req.name, email, hashed_password)
            result = await self.db_service.execute(query, params)
            new_user_id = result[0].get('last_insert_id')
            user = await self.get_user_by_id(new_user_id, _already_connected=True)
            if not user:
                raise ValueError("No se pudo crear el usuario")
            return user
        except Exception as e:
            logging.error(f"Error registrando usuario: {str(e)}")
            raise
        finally:
            try:
                await self.db_service.disconnect()
            except Exception:
                pass

    async def authenticate_from_encrypted(self, req: LoginRequest) -> Optional[UserResponse]:
        """Autentica un usuario recibiendo email y password encriptados (Fernet)."""
        try:
            await self.db_service.connect()
            email = decrypt_text(req.email_encrypted).strip().lower()
            password = decrypt_text(req.password_encrypted)
            user_row = await self._get_user_row_by_email(email)
            if not user_row:
                return None
            hashed = user_row.get('password')
            if not hashed:
                return None
            if not self.verify_password(password, hashed):
                return None
            # Construir UserResponse sin el campo password
            return UserResponse(
                id=user_row['id'],
                name=user_row['name'],
                email=user_row['email'],
                email_verified_at=user_row.get('email_verified_at'),
                created_at=user_row.get('created_at'),
                updated_at=user_row.get('updated_at'),
            )
        except Exception as e:
            logging.error(f"Error autenticando usuario: {str(e)}")
            raise
        finally:
            try:
                await self.db_service.disconnect()
            except Exception:
                pass

    async def _get_user_row_by_email(self, email: str, _already_connected: bool = True) -> Optional[dict]:
        """Obtiene la fila completa incluyendo password."""
        if not _already_connected:
            await self.db_service.connect()
        try:
            query = "SELECT * FROM users WHERE email = %s"
            rows = await self.db_service.execute(query, (email,))
            return rows[0] if rows else None
        finally:
            if not _already_connected:
                await self.db_service.disconnect()

    async def get_user_by_email(self, email: str, _already_connected: bool = False) -> Optional[UserResponse]:
        if not _already_connected:
            await self.db_service.connect()
        try:
            query = "SELECT id, name, email, email_verified_at, created_at, updated_at FROM users WHERE email = %s"
            result = await self.db_service.execute(query, (email,))
            if result:
                return UserResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving user by email: {str(e)}")
            raise
        finally:
            if not _already_connected:
                try:
                    await self.db_service.disconnect()
                except Exception:
                    pass

    async def get_user_by_id(self, user_id: int, _already_connected: bool = False) -> Optional[UserResponse]:
        try:
            if not _already_connected:
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
            if not _already_connected:
                await self.db_service.disconnect()

    # Todo: Aquí irían los métodos get_all_users, update_user y delete_user, siguiendo el mismo patrón que en los otros servicios.