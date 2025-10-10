import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.location_models import LocationCreate, LocationUpdate, LocationResponse


class LocationService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_location(self, location: LocationCreate) -> LocationResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO locations (location_name, address, city, country, location_type, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (location.location_name, location.address, location.city, location.country, location.location_type.value)
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM locations WHERE location_name = %s ORDER BY id DESC LIMIT 1"
            result = await self.db_service.execute(select_query, (location.location_name,))

            if result:
                return LocationResponse(**result[0])
            raise ValueError("Location creation failed")
        except Exception as e:
            logging.error(f"Error creating location: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_location_by_id(self, location_id: int) -> Optional[LocationResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM locations WHERE id = %s"
            result = await self.db_service.execute(query, (location_id,))

            if result:
                return LocationResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving location: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_locations(self, limit: int = 100, offset: int = 0) -> List[LocationResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM locations LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [LocationResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving locations: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_location(self, location_id: int, location: LocationUpdate) -> Optional[LocationResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if location.location_name is not None:
                update_fields.append("location_name = %s")
                params.append(location.location_name)
            if location.address is not None:
                update_fields.append("address = %s")
                params.append(location.address)
            if location.city is not None:
                update_fields.append("city = %s")
                params.append(location.city)
            if location.country is not None:
                update_fields.append("country = %s")
                params.append(location.country)
            if location.location_type is not None:
                update_fields.append("location_type = %s")
                params.append(location.location_type.value)

            if not update_fields:
                return await self.get_location_by_id(location_id)

            update_fields.append("updated_at = NOW()")
            params.append(location_id)

            query = f"UPDATE locations SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_location_by_id(location_id)
        except Exception as e:
            logging.error(f"Error updating location: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_location(self, location_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM locations WHERE id = %s"
            await self.db_service.execute(query, (location_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting location: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

