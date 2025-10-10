import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.asset_models import AssetCreate, AssetUpdate, AssetResponse


class AssetService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_asset(self, asset: AssetCreate) -> AssetResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO assets (asset_code, asset_type_id, ownership, status, size, `condition`, 
                                   category, manufactured_at, last_maintenance_at, last_inspection_at, 
                                   next_inspection_due_at, max_payload_kg, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (
                asset.asset_code, asset.asset_type_id, asset.ownership.value, asset.status.value,
                asset.size.value, asset.condition.value, asset.category.value, asset.manufactured_at,
                asset.last_maintenance_at, asset.last_inspection_at, asset.next_inspection_due_at,
                asset.max_payload_kg
            )
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM assets WHERE asset_code = %s"
            result = await self.db_service.execute(select_query, (asset.asset_code,))

            if result:
                return AssetResponse(**result[0])
            raise ValueError("Asset creation failed")
        except Exception as e:
            logging.error(f"Error creating asset: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_asset_by_id(self, asset_id: int) -> Optional[AssetResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM assets WHERE id = %s"
            result = await self.db_service.execute(query, (asset_id,))

            if result:
                return AssetResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving asset: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_assets(self, limit: int = 100, offset: int = 0) -> List[AssetResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM assets LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [AssetResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving assets: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_asset(self, asset_id: int, asset: AssetUpdate) -> Optional[AssetResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if asset.asset_code is not None:
                update_fields.append("asset_code = %s")
                params.append(asset.asset_code)
            if asset.asset_type_id is not None:
                update_fields.append("asset_type_id = %s")
                params.append(asset.asset_type_id)
            if asset.ownership is not None:
                update_fields.append("ownership = %s")
                params.append(asset.ownership.value)
            if asset.status is not None:
                update_fields.append("status = %s")
                params.append(asset.status.value)
            if asset.size is not None:
                update_fields.append("size = %s")
                params.append(asset.size.value)
            if asset.condition is not None:
                update_fields.append("`condition` = %s")
                params.append(asset.condition.value)
            if asset.category is not None:
                update_fields.append("category = %s")
                params.append(asset.category.value)
            if asset.manufactured_at is not None:
                update_fields.append("manufactured_at = %s")
                params.append(asset.manufactured_at)
            if asset.last_maintenance_at is not None:
                update_fields.append("last_maintenance_at = %s")
                params.append(asset.last_maintenance_at)
            if asset.last_inspection_at is not None:
                update_fields.append("last_inspection_at = %s")
                params.append(asset.last_inspection_at)
            if asset.next_inspection_due_at is not None:
                update_fields.append("next_inspection_due_at = %s")
                params.append(asset.next_inspection_due_at)
            if asset.max_payload_kg is not None:
                update_fields.append("max_payload_kg = %s")
                params.append(asset.max_payload_kg)

            if not update_fields:
                return await self.get_asset_by_id(asset_id)

            update_fields.append("updated_at = NOW()")
            params.append(asset_id)

            query = f"UPDATE assets SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_asset_by_id(asset_id)
        except Exception as e:
            logging.error(f"Error updating asset: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_asset(self, asset_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM assets WHERE id = %s"
            await self.db_service.execute(query, (asset_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting asset: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

