import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.route_models import RouteCreate, RouteUpdate, RouteResponse


class RouteService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_route(self, route: RouteCreate) -> RouteResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO routes (origin_location_id, destination_location_id, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
            """
            params = (route.origin_location_id, route.destination_location_id)
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM routes WHERE origin_location_id = %s AND destination_location_id = %s ORDER BY id DESC LIMIT 1"
            result = await self.db_service.execute(select_query, (route.origin_location_id, route.destination_location_id))

            if result:
                return RouteResponse(**result[0])
            raise ValueError("Route creation failed")
        except Exception as e:
            logging.error(f"Error creating route: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_route_by_id(self, route_id: int) -> Optional[RouteResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM routes WHERE id = %s"
            result = await self.db_service.execute(query, (route_id,))

            if result:
                return RouteResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving route: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_routes(self, limit: int = 100, offset: int = 0) -> List[RouteResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM routes LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [RouteResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving routes: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_route(self, route_id: int, route: RouteUpdate) -> Optional[RouteResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if route.origin_location_id is not None:
                update_fields.append("origin_location_id = %s")
                params.append(route.origin_location_id)
            if route.destination_location_id is not None:
                update_fields.append("destination_location_id = %s")
                params.append(route.destination_location_id)

            if not update_fields:
                return await self.get_route_by_id(route_id)

            update_fields.append("updated_at = NOW()")
            params.append(route_id)

            query = f"UPDATE routes SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_route_by_id(route_id)
        except Exception as e:
            logging.error(f"Error updating route: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_route(self, route_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM routes WHERE id = %s"
            await self.db_service.execute(query, (route_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting route: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

