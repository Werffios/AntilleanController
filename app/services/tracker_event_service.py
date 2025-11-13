import logging
from typing import List, Optional
from app.database.mongo_manager import MongoManager
from app.models.tracker_event_models import TrackerEventResponse


class TrackerEventService:
    def __init__(self):
        self.mongo_manager = MongoManager()
        self.collection_name = "HoopoMessages"

    async def get_all_tracker_events(self, limit: int = 100, offset: int = 0) -> List[TrackerEventResponse]:
        """
        Retrieves all tracker events with pagination
        """
        try:
            await self.mongo_manager.create_connection()
            collection = await self.mongo_manager.get_collection(self.collection_name)


            cursor = collection.find().skip(offset).limit(limit)
            events = await cursor.to_list(length=limit)

            # Convert ObjectId to string for response
            result = []
            for event in events:
                event['_id'] = str(event['_id'])
                result.append(TrackerEventResponse(**event))

            return result
        except Exception as e:
            logging.error(f"Error retrieving tracker events: {str(e)}")
            raise
        finally:
            await self.mongo_manager.close_connection()

    async def get_tracker_events_by_date_range(
            self,
            tracker_id: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            limit: int = 100,
            offset: int = 0
    ) -> List[TrackerEventResponse]:
        """
        Retrieves tracker events for a specific TrackerId within a date range
        """
        try:
            from datetime import datetime, timezone

            # Set default dates to today if not provided
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            start_date = start_date or today
            end_date = end_date or today

            # Parse dates and create datetime objects
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d").replace(
                hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
            )
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc
            )

            await self.mongo_manager.create_connection()
            collection = await self.mongo_manager.get_collection(self.collection_name)

            # Build query with tracker_id and date range
            query = {
                "TrackerId": tracker_id,
                "EventTime": {
                    "$gte": start_datetime,
                    "$lte": end_datetime
                }
            }

            cursor = collection.find(query).sort("EventTime", -1).skip(offset).limit(limit)
            events = await cursor.to_list(length=limit)

            # Convert ObjectId to string for response
            result = []
            for event in events:
                event['_id'] = str(event['_id'])
                result.append(TrackerEventResponse(**event))

            return result
        except ValueError as e:
            logging.error(f"Date parsing error: {str(e)}")
            raise ValueError("Invalid date format. Use YYYY-MM-DD format.")
        except Exception as e:
            logging.error(f"Error retrieving tracker events by date range: {str(e)}")
            raise
        finally:
            await self.mongo_manager.close_connection()

    async def get_tracker_events_by_tracker_id(self, tracker_id: str, limit: int = 100, offset: int = 0) -> List[
        TrackerEventResponse]:
        """
        Retrieves tracker events for a specific TrackerId with pagination
        """
        try:
            await self.mongo_manager.create_connection()
            collection = await self.mongo_manager.get_collection(self.collection_name)

            cursor = collection.find({"AssetName": tracker_id}).sort("EventTime", -1).skip(offset).limit(limit)
            events = await cursor.to_list(length=limit)

            # Convert ObjectId to string for response
            result = []
            for event in events:
                event['_id'] = str(event['_id'])
                result.append(TrackerEventResponse(**event))

            return result
        except Exception as e:
            logging.error(f"Error retrieving tracker events by tracker_id: {str(e)}")
            raise
        finally:
            await self.mongo_manager.close_connection()

    async def get_tracker_event_by_id(self, event_id: str) -> Optional[TrackerEventResponse]:
        """
        Retrieves a specific tracker event by its MongoDB _id
        """
        try:
            from bson import ObjectId
            await self.mongo_manager.create_connection()
            collection = await self.mongo_manager.get_collection(self.collection_name)

            event = await collection.find_one({"_id": ObjectId(event_id)})

            if event:
                event['_id'] = str(event['_id'])
                return TrackerEventResponse(**event)
            return None
        except Exception as e:
            logging.error(f"Error retrieving tracker event by id: {str(e)}")
            raise
        finally:
            await self.mongo_manager.close_connection()

    async def count_tracker_events(self) -> int:
        """
        Returns the total count of tracker events
        """
        try:
            await self.mongo_manager.create_connection()
            collection = await self.mongo_manager.get_collection(self.collection_name)
            count = await collection.count_documents({})
            return count
        except Exception as e:
            logging.error(f"Error counting tracker events: {str(e)}")
            raise
        finally:
            await self.mongo_manager.close_connection()

    async def count_tracker_events_by_tracker_id(self, tracker_id: str) -> int:
        """
        Returns the count of tracker events for a specific TrackerId
        """
        try:
            await self.mongo_manager.create_connection()
            collection = await self.mongo_manager.get_collection(self.collection_name)
            count = await collection.count_documents({"TrackerId": tracker_id})
            return count
        except Exception as e:
            logging.error(f"Error counting tracker events by tracker_id: {str(e)}")
            raise
        finally:
            await self.mongo_manager.close_connection()

