import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.tracker_models import TrackerCreate, TrackerUpdate, TrackerResponse


class TrackerService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_tracker(self, tracker: TrackerCreate) -> TrackerResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO trackers (tracker_code, created_at, updated_at)
                VALUES (%s, NOW(), NOW())
            """
            params = (tracker.tracker_code,)
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM trackers WHERE tracker_code = %s ORDER BY id DESC LIMIT 1"
            result = await self.db_service.execute(select_query, (tracker.tracker_code,))

            if result:
                return TrackerResponse(**result[0])
            raise ValueError("Tracker creation failed")
        except Exception as e:
            logging.error(f"Error creating tracker: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_tracker_by_id(self, tracker_id: int) -> Optional[TrackerResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM trackers WHERE id = %s"
            result = await self.db_service.execute(query, (tracker_id,))

            if result:
                return TrackerResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving tracker: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_tracker_by_code(self, tracker_code: str) -> Optional[TrackerResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM trackers WHERE tracker_code = %s"
            result = await self.db_service.execute(query, (tracker_code,))

            if result:
                return TrackerResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving tracker by code: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_trackers(self, limit: int = 100, offset: int = 0) -> List[TrackerResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM trackers LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [TrackerResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving trackers: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_tracker(self, tracker_id: int, tracker: TrackerUpdate) -> Optional[TrackerResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if tracker.tracker_code is not None:
                update_fields.append("tracker_code = %s")
                params.append(tracker.tracker_code)

            if not update_fields:
                return await self.get_tracker_by_id(tracker_id)

            update_fields.append("updated_at = NOW()")
            params.append(tracker_id)

            query = f"UPDATE trackers SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_tracker_by_id(tracker_id)
        except Exception as e:
            logging.error(f"Error updating tracker: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_tracker(self, tracker_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM trackers WHERE id = %s"
            await self.db_service.execute(query, (tracker_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting tracker: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()
