import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.maintenance_models import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse


class MaintenanceService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_maintenance(self, maintenance: MaintenanceCreate) -> MaintenanceResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO maintenances (asset_id, maintenance_type, status, description,
                                         service_provider, cost, scheduled_at, started_at,
                                         completed_at, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (
                maintenance.asset_id, maintenance.maintenance_type.value, maintenance.status.value,
                maintenance.description, maintenance.service_provider, maintenance.cost,
                maintenance.scheduled_at, maintenance.started_at, maintenance.completed_at
            )
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM maintenances WHERE id = LAST_INSERT_ID()"
            result = await self.db_service.execute(select_query, ())

            if result:
                return MaintenanceResponse(**result[0])
            raise ValueError("Maintenance creation failed")
        except Exception as e:
            logging.error(f"Error creating maintenance: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_maintenance_by_id(self, maintenance_id: int) -> Optional[MaintenanceResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM maintenances WHERE id = %s"
            result = await self.db_service.execute(query, (maintenance_id,))

            if result:
                return MaintenanceResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving maintenance: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_maintenances(self, limit: int = 100, offset: int = 0) -> List[MaintenanceResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM maintenances LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [MaintenanceResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving maintenances: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_maintenances_by_asset(self, asset_id: int) -> List[MaintenanceResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM maintenances WHERE asset_id = %s"
            result = await self.db_service.execute(query, (asset_id,))

            return [MaintenanceResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving maintenances by asset: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_maintenances_by_status(self, status: str) -> List[MaintenanceResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM maintenances WHERE status = %s"
            result = await self.db_service.execute(query, (status,))

            return [MaintenanceResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving maintenances by status: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_maintenances_by_type(self, maintenance_type: str) -> List[MaintenanceResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM maintenances WHERE maintenance_type = %s"
            result = await self.db_service.execute(query, (maintenance_type,))

            return [MaintenanceResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving maintenances by type: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_maintenance(self, maintenance_id: int, maintenance: MaintenanceUpdate) -> Optional[MaintenanceResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if maintenance.asset_id is not None:
                update_fields.append("asset_id = %s")
                params.append(maintenance.asset_id)
            if maintenance.maintenance_type is not None:
                update_fields.append("maintenance_type = %s")
                params.append(maintenance.maintenance_type.value)
            if maintenance.status is not None:
                update_fields.append("status = %s")
                params.append(maintenance.status.value)
            if maintenance.description is not None:
                update_fields.append("description = %s")
                params.append(maintenance.description)
            if maintenance.service_provider is not None:
                update_fields.append("service_provider = %s")
                params.append(maintenance.service_provider)
            if maintenance.cost is not None:
                update_fields.append("cost = %s")
                params.append(maintenance.cost)
            if maintenance.scheduled_at is not None:
                update_fields.append("scheduled_at = %s")
                params.append(maintenance.scheduled_at)
            if maintenance.started_at is not None:
                update_fields.append("started_at = %s")
                params.append(maintenance.started_at)
            if maintenance.completed_at is not None:
                update_fields.append("completed_at = %s")
                params.append(maintenance.completed_at)

            if not update_fields:
                return await self.get_maintenance_by_id(maintenance_id)

            update_fields.append("updated_at = NOW()")
            params.append(maintenance_id)

            query = f"UPDATE maintenances SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_maintenance_by_id(maintenance_id)
        except Exception as e:
            logging.error(f"Error updating maintenance: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_maintenance(self, maintenance_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM maintenances WHERE id = %s"
            await self.db_service.execute(query, (maintenance_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting maintenance: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

