import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.asset_type_models import AssetTypeCreate, AssetTypeUpdate, AssetTypeResponse


class AssetTypeService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_asset_type(self, asset_type: AssetTypeCreate) -> AssetTypeResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO asset_types (type_name, created_at, updated_at)
                VALUES (%s, NOW(), NOW())
            """
            params = (asset_type.type_name,)
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM asset_types WHERE type_name = %s ORDER BY id DESC LIMIT 1"
            result = await self.db_service.execute(select_query, (asset_type.type_name,))

            if result:
                return AssetTypeResponse(**result[0])
            raise ValueError("Asset type creation failed")
        except Exception as e:
            logging.error(f"Error creating asset type: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_asset_type_by_id(self, asset_type_id: int) -> Optional[AssetTypeResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM asset_types WHERE id = %s"
            result = await self.db_service.execute(query, (asset_type_id,))

            if result:
                return AssetTypeResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving asset type: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_asset_types(self, limit: int = 100, offset: int = 0) -> List[AssetTypeResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM asset_types LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [AssetTypeResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving asset types: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_asset_type(self, asset_type_id: int, asset_type: AssetTypeUpdate) -> Optional[AssetTypeResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if asset_type.type_name is not None:
                update_fields.append("type_name = %s")
                params.append(asset_type.type_name)

            if not update_fields:
                return await self.get_asset_type_by_id(asset_type_id)

            update_fields.append("updated_at = NOW()")
            params.append(asset_type_id)

            query = f"UPDATE asset_types SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_asset_type_by_id(asset_type_id)
        except Exception as e:
            logging.error(f"Error updating asset type: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_asset_type(self, asset_type_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM asset_types WHERE id = %s"
            await self.db_service.execute(query, (asset_type_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting asset type: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

