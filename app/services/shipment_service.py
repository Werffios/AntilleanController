import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.shipment_models import ShipmentCreate, ShipmentUpdate, ShipmentResponse


class ShipmentService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_shipment(self, shipment: ShipmentCreate) -> ShipmentResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO shipments (tracking_code, customer_id, voyage_id, origin_location_id,
                                      destination_location_id, creation_datetime, declared_value,
                                      current_status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (
                shipment.tracking_code, shipment.customer_id, shipment.voyage_id,
                shipment.origin_location_id, shipment.destination_location_id,
                shipment.creation_datetime, shipment.declared_value, shipment.current_status
            )
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM shipments WHERE tracking_code = %s"
            result = await self.db_service.execute(select_query, (shipment.tracking_code,))

            if result:
                return ShipmentResponse(**result[0])
            raise ValueError("Shipment creation failed")
        except Exception as e:
            logging.error(f"Error creating shipment: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_shipment_by_id(self, shipment_id: int) -> Optional[ShipmentResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM shipments WHERE id = %s"
            result = await self.db_service.execute(query, (shipment_id,))

            if result:
                return ShipmentResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving shipment: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_shipment_by_tracking_code(self, tracking_code: str) -> Optional[ShipmentResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM shipments WHERE tracking_code = %s"
            result = await self.db_service.execute(query, (tracking_code,))

            if result:
                return ShipmentResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving shipment by tracking code: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_shipments(self, limit: int = 100, offset: int = 0) -> List[ShipmentResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM shipments LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [ShipmentResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving shipments: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_shipments_by_customer(self, customer_id: int) -> List[ShipmentResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM shipments WHERE customer_id = %s"
            result = await self.db_service.execute(query, (customer_id,))

            return [ShipmentResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving shipments by customer: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_shipments_by_voyage(self, voyage_id: int) -> List[ShipmentResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM shipments WHERE voyage_id = %s"
            result = await self.db_service.execute(query, (voyage_id,))

            return [ShipmentResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving shipments by voyage: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_shipment(self, shipment_id: int, shipment: ShipmentUpdate) -> Optional[ShipmentResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if shipment.tracking_code is not None:
                update_fields.append("tracking_code = %s")
                params.append(shipment.tracking_code)
            if shipment.customer_id is not None:
                update_fields.append("customer_id = %s")
                params.append(shipment.customer_id)
            if shipment.voyage_id is not None:
                update_fields.append("voyage_id = %s")
                params.append(shipment.voyage_id)
            if shipment.origin_location_id is not None:
                update_fields.append("origin_location_id = %s")
                params.append(shipment.origin_location_id)
            if shipment.destination_location_id is not None:
                update_fields.append("destination_location_id = %s")
                params.append(shipment.destination_location_id)
            if shipment.creation_datetime is not None:
                update_fields.append("creation_datetime = %s")
                params.append(shipment.creation_datetime)
            if shipment.declared_value is not None:
                update_fields.append("declared_value = %s")
                params.append(shipment.declared_value)
            if shipment.current_status is not None:
                update_fields.append("current_status = %s")
                params.append(shipment.current_status)

            if not update_fields:
                return await self.get_shipment_by_id(shipment_id)

            update_fields.append("updated_at = NOW()")
            params.append(shipment_id)

            query = f"UPDATE shipments SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_shipment_by_id(shipment_id)
        except Exception as e:
            logging.error(f"Error updating shipment: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_shipment(self, shipment_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM shipments WHERE id = %s"
            await self.db_service.execute(query, (shipment_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting shipment: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()
