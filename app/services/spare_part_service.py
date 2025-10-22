import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.spare_part_models import SparePartCreate, SparePartUpdate, SparePartResponse


class SparePartService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_spare_part(self, part: SparePartCreate) -> SparePartResponse:
        try:
            await self.db_service.connect()
            query = (
                """
                INSERT INTO spare_parts (name, part_number, manufacturer, quantity, unit_cost, location, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                """
            )
            params = (
                part.name, part.part_number, part.manufacturer, part.quantity, part.unit_cost, part.location
            )
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM spare_parts WHERE part_number = %s"
            result = await self.db_service.execute(select_query, (part.part_number,))

            if result:
                return SparePartResponse(**result[0])
            raise ValueError("Spare part creation failed")
        except Exception as e:
            logging.error(f"Error creating spare part: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_spare_part_by_id(self, part_id: int) -> Optional[SparePartResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM spare_parts WHERE id = %s"
            result = await self.db_service.execute(query, (part_id,))

            if result:
                return SparePartResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving spare part: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_spare_parts(self, limit: int = 100, offset: int = 0) -> List[SparePartResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM spare_parts LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [SparePartResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving spare parts: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_spare_part(self, part_id: int, part: SparePartUpdate) -> Optional[SparePartResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if part.name is not None:
                update_fields.append("name = %s")
                params.append(part.name)
            if part.part_number is not None:
                update_fields.append("part_number = %s")
                params.append(part.part_number)
            if part.manufacturer is not None:
                update_fields.append("manufacturer = %s")
                params.append(part.manufacturer)
            if part.quantity is not None:
                update_fields.append("quantity = %s")
                params.append(part.quantity)
            if part.unit_cost is not None:
                update_fields.append("unit_cost = %s")
                params.append(part.unit_cost)
            if part.location is not None:
                update_fields.append("location = %s")
                params.append(part.location)

            if not update_fields:
                return await self.get_spare_part_by_id(part_id)

            update_fields.append("updated_at = NOW()")
            params.append(part_id)

            query = f"UPDATE spare_parts SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_spare_part_by_id(part_id)
        except Exception as e:
            logging.error(f"Error updating spare part: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_spare_part(self, part_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM spare_parts WHERE id = %s"
            await self.db_service.execute(query, (part_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting spare part: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

