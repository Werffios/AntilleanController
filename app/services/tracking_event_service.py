import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.tracking_event_models import TrackingEventCreate, TrackingEventUpdate, TrackingEventResponse


class TrackingEventService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_tracking_event(self, tracking_event: TrackingEventCreate) -> TrackingEventResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO tracking_events (shipment_id, location_id, event_datetime, event_type, notes, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (
                tracking_event.shipment_id,
                tracking_event.location_id,
                tracking_event.event_datetime,
                tracking_event.event_type,
                tracking_event.notes
            )
            await self.db_service.execute(query, params)

            select_query = """
                SELECT * FROM tracking_events 
                WHERE shipment_id = %s AND event_datetime = %s 
                ORDER BY id DESC LIMIT 1
            """
            result = await self.db_service.execute(
                select_query,
                (tracking_event.shipment_id, tracking_event.event_datetime)
            )

            if result:
                return TrackingEventResponse(**result[0])
            raise ValueError("Tracking event creation failed")
        except Exception as e:
            logging.error(f"Error creating tracking event: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_tracking_event_by_id(self, tracking_event_id: int) -> Optional[TrackingEventResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM tracking_events WHERE id = %s"
            result = await self.db_service.execute(query, (tracking_event_id,))

            if result:
                return TrackingEventResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving tracking event: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_tracking_events_by_shipment(self, shipment_id: int) -> List[TrackingEventResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM tracking_events WHERE shipment_id = %s ORDER BY event_datetime DESC"
            result = await self.db_service.execute(query, (shipment_id,))

            return [TrackingEventResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving tracking events by shipment: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_tracking_events(self, limit: int = 100, offset: int = 0) -> List[TrackingEventResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM tracking_events ORDER BY event_datetime DESC LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [TrackingEventResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving tracking events: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_tracking_event(self, tracking_event_id: int, tracking_event: TrackingEventUpdate) -> Optional[TrackingEventResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if tracking_event.shipment_id is not None:
                update_fields.append("shipment_id = %s")
                params.append(tracking_event.shipment_id)
            if tracking_event.location_id is not None:
                update_fields.append("location_id = %s")
                params.append(tracking_event.location_id)
            if tracking_event.event_datetime is not None:
                update_fields.append("event_datetime = %s")
                params.append(tracking_event.event_datetime)
            if tracking_event.event_type is not None:
                update_fields.append("event_type = %s")
                params.append(tracking_event.event_type)
            if tracking_event.notes is not None:
                update_fields.append("notes = %s")
                params.append(tracking_event.notes)

            if not update_fields:
                return await self.get_tracking_event_by_id(tracking_event_id)

            update_fields.append("updated_at = NOW()")
            params.append(tracking_event_id)

            query = f"UPDATE tracking_events SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_tracking_event_by_id(tracking_event_id)
        except Exception as e:
            logging.error(f"Error updating tracking event: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_tracking_event(self, tracking_event_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM tracking_events WHERE id = %s"
            await self.db_service.execute(query, (tracking_event_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting tracking event: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()
