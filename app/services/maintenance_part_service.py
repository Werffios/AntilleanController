import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.maintenance_part_models import (
    MaintenancePartCreate,
    MaintenancePartUpdate,
    MaintenancePartResponse,
)


class MaintenancePartService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_maintenance_part(self, item: MaintenancePartCreate) -> MaintenancePartResponse:
        try:
            await self.db_service.connect()
            query = (
                """
                INSERT INTO maintenance_parts (maintenance_id, spare_part_id, quantity_used, cost_at_consumption, created_at)
                VALUES (%s, %s, %s, %s, NOW())
                """
            )
            params = (
                item.maintenance_id,
                item.spare_part_id,
                item.quantity_used,
                item.cost_at_consumption,
            )
            await self.db_service.execute(query, params)

            select_query = (
                "SELECT * FROM maintenance_parts WHERE maintenance_id = %s AND spare_part_id = %s"
            )
            result = await self.db_service.execute(
                select_query, (item.maintenance_id, item.spare_part_id)
            )

            if result:
                return MaintenancePartResponse(**result[0])
            raise ValueError("Maintenance part creation failed")
        except Exception as e:
            logging.error(f"Error creating maintenance part: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_maintenance_part(self, maintenance_id: int, spare_part_id: int) -> Optional[MaintenancePartResponse]:
        try:
            await self.db_service.connect()
            query = (
                "SELECT * FROM maintenance_parts WHERE maintenance_id = %s AND spare_part_id = %s"
            )
            result = await self.db_service.execute(query, (maintenance_id, spare_part_id))

            if result:
                return MaintenancePartResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving maintenance part: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_maintenance_parts(self, limit: int = 100, offset: int = 0) -> List[MaintenancePartResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM maintenance_parts LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [MaintenancePartResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving maintenance parts: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_maintenance_parts_by_maintenance(self, maintenance_id: int, limit: int = 100, offset: int = 0) -> List[MaintenancePartResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM maintenance_parts WHERE maintenance_id = %s LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (maintenance_id, limit, offset))

            return [MaintenancePartResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving maintenance parts by maintenance: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_maintenance_parts_by_spare_part(self, spare_part_id: int, limit: int = 100, offset: int = 0) -> List[MaintenancePartResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM maintenance_parts WHERE spare_part_id = %s LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (spare_part_id, limit, offset))

            return [MaintenancePartResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving maintenance parts by spare part: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_maintenance_part(self, maintenance_id: int, spare_part_id: int, item: MaintenancePartUpdate) -> Optional[MaintenancePartResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if item.quantity_used is not None:
                update_fields.append("quantity_used = %s")
                params.append(item.quantity_used)
            if item.cost_at_consumption is not None:
                update_fields.append("cost_at_consumption = %s")
                params.append(item.cost_at_consumption)

            if not update_fields:
                return await self.get_maintenance_part(maintenance_id, spare_part_id)

            params.extend([maintenance_id, spare_part_id])

            query = (
                f"UPDATE maintenance_parts SET {', '.join(update_fields)} WHERE maintenance_id = %s AND spare_part_id = %s"
            )
            await self.db_service.execute(query, tuple(params))

            return await self.get_maintenance_part(maintenance_id, spare_part_id)
        except Exception as e:
            logging.error(f"Error updating maintenance part: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_maintenance_part(self, maintenance_id: int, spare_part_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM maintenance_parts WHERE maintenance_id = %s AND spare_part_id = %s"
            await self.db_service.execute(query, (maintenance_id, spare_part_id))
            return True
        except Exception as e:
            logging.error(f"Error deleting maintenance part: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

