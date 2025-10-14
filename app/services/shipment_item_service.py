import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.shipment_item_models import ShipmentItemCreate, ShipmentItemUpdate, ShipmentItemResponse


class ShipmentItemService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_shipment_item(self, item: ShipmentItemCreate) -> ShipmentItemResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO shipment_items (shipment_id, asset_id, description, weight_kg, dimensions, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (
                item.shipment_id,
                item.asset_id,
                item.description,
                item.weight_kg,
                item.dimensions
            )
            await self.db_service.execute(query, params)

            select_query = """
                SELECT * FROM shipment_items 
                WHERE shipment_id = %s AND asset_id = %s 
                ORDER BY id DESC LIMIT 1
            """
            result = await self.db_service.execute(select_query, (item.shipment_id, item.asset_id))

            if result:
                return ShipmentItemResponse(**result[0])
            raise ValueError("Shipment item creation failed")
        except Exception as e:
            logging.error(f"Error creating shipment item: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_shipment_item_by_id(self, item_id: int) -> Optional[ShipmentItemResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM shipment_items WHERE id = %s"
            result = await self.db_service.execute(query, (item_id,))

            if result:
                return ShipmentItemResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving shipment item: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_shipment_items_by_shipment(self, shipment_id: int) -> List[ShipmentItemResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM shipment_items WHERE shipment_id = %s"
            result = await self.db_service.execute(query, (shipment_id,))

            return [ShipmentItemResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving shipment items by shipment: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_shipment_items_by_asset(self, asset_id: int) -> List[ShipmentItemResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM shipment_items WHERE asset_id = %s"
            result = await self.db_service.execute(query, (asset_id,))

            return [ShipmentItemResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving shipment items by asset: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_shipment_items(self, limit: int = 100, offset: int = 0) -> List[ShipmentItemResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM shipment_items LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [ShipmentItemResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving shipment items: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_shipment_item(self, item_id: int, item: ShipmentItemUpdate) -> Optional[ShipmentItemResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if item.shipment_id is not None:
                update_fields.append("shipment_id = %s")
                params.append(item.shipment_id)
            if item.asset_id is not None:
                update_fields.append("asset_id = %s")
                params.append(item.asset_id)
            if item.description is not None:
                update_fields.append("description = %s")
                params.append(item.description)
            if item.weight_kg is not None:
                update_fields.append("weight_kg = %s")
                params.append(item.weight_kg)
            if item.dimensions is not None:
                update_fields.append("dimensions = %s")
                params.append(item.dimensions)

            if not update_fields:
                return await self.get_shipment_item_by_id(item_id)

            update_fields.append("updated_at = NOW()")
            params.append(item_id)

            query = f"UPDATE shipment_items SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_shipment_item_by_id(item_id)
        except Exception as e:
            logging.error(f"Error updating shipment item: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_shipment_item(self, item_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM shipment_items WHERE id = %s"
            await self.db_service.execute(query, (item_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting shipment item: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()
