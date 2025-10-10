import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.voyage_models import VoyageCreate, VoyageUpdate, VoyageResponse


class VoyageService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_voyage(self, voyage: VoyageCreate) -> VoyageResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO voyages (route_id, vessel_id, departure_datetime, arrival_datetime,
                                    status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (
                voyage.route_id, voyage.vessel_id, voyage.departure_datetime,
                voyage.arrival_datetime, voyage.status
            )
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM voyages WHERE route_id = %s AND vessel_id = %s ORDER BY id DESC LIMIT 1"
            result = await self.db_service.execute(select_query, (voyage.route_id, voyage.vessel_id))

            if result:
                return VoyageResponse(**result[0])
            raise ValueError("Voyage creation failed")
        except Exception as e:
            logging.error(f"Error creating voyage: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_voyage_by_id(self, voyage_id: int) -> Optional[VoyageResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM voyages WHERE id = %s"
            result = await self.db_service.execute(query, (voyage_id,))

            if result:
                return VoyageResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving voyage: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_voyages(self, limit: int = 100, offset: int = 0) -> List[VoyageResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM voyages LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [VoyageResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving voyages: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_voyages_by_vessel(self, vessel_id: int) -> List[VoyageResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM voyages WHERE vessel_id = %s"
            result = await self.db_service.execute(query, (vessel_id,))

            return [VoyageResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving voyages by vessel: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_voyage(self, voyage_id: int, voyage: VoyageUpdate) -> Optional[VoyageResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if voyage.route_id is not None:
                update_fields.append("route_id = %s")
                params.append(voyage.route_id)
            if voyage.vessel_id is not None:
                update_fields.append("vessel_id = %s")
                params.append(voyage.vessel_id)
            if voyage.departure_datetime is not None:
                update_fields.append("departure_datetime = %s")
                params.append(voyage.departure_datetime)
            if voyage.arrival_datetime is not None:
                update_fields.append("arrival_datetime = %s")
                params.append(voyage.arrival_datetime)
            if voyage.status is not None:
                update_fields.append("status = %s")
                params.append(voyage.status)

            if not update_fields:
                return await self.get_voyage_by_id(voyage_id)

            update_fields.append("updated_at = NOW()")
            params.append(voyage_id)

            query = f"UPDATE voyages SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_voyage_by_id(voyage_id)
        except Exception as e:
            logging.error(f"Error updating voyage: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_voyage(self, voyage_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM voyages WHERE id = %s"
            await self.db_service.execute(query, (voyage_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting voyage: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

