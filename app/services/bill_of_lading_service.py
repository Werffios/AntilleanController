import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.bill_of_lading_models import BillOfLadingCreate, BillOfLadingUpdate, BillOfLadingResponse


class BillOfLadingService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_bill_of_lading(self, bill: BillOfLadingCreate) -> BillOfLadingResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO bills_of_lading (shipment_id, bol_number, issue_date, terms_and_conditions,
                                            shipper_details, consignee_details, is_hazardous, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (
                bill.shipment_id,
                bill.bol_number,
                bill.issue_date,
                bill.terms_and_conditions,
                bill.shipper_details,
                bill.consignee_details,
                bill.is_hazardous
            )
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM bills_of_lading WHERE bol_number = %s"
            result = await self.db_service.execute(select_query, (bill.bol_number,))

            if result:
                return BillOfLadingResponse(**result[0])
            raise ValueError("Bill of lading creation failed")
        except Exception as e:
            logging.error(f"Error creating bill of lading: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_bill_of_lading_by_id(self, bill_id: int) -> Optional[BillOfLadingResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM bills_of_lading WHERE id = %s"
            result = await self.db_service.execute(query, (bill_id,))

            if result:
                return BillOfLadingResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving bill of lading: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_bill_of_lading_by_bol_number(self, bol_number: str) -> Optional[BillOfLadingResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM bills_of_lading WHERE bol_number = %s"
            result = await self.db_service.execute(query, (bol_number,))

            if result:
                return BillOfLadingResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving bill of lading by number: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_bill_of_lading_by_shipment(self, shipment_id: int) -> Optional[BillOfLadingResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM bills_of_lading WHERE shipment_id = %s"
            result = await self.db_service.execute(query, (shipment_id,))

            if result:
                return BillOfLadingResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving bill of lading by shipment: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_bills_of_lading(self, limit: int = 100, offset: int = 0) -> List[BillOfLadingResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM bills_of_lading LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [BillOfLadingResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving bills of lading: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_bill_of_lading(self, bill_id: int, bill: BillOfLadingUpdate) -> Optional[BillOfLadingResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if bill.shipment_id is not None:
                update_fields.append("shipment_id = %s")
                params.append(bill.shipment_id)
            if bill.bol_number is not None:
                update_fields.append("bol_number = %s")
                params.append(bill.bol_number)
            if bill.issue_date is not None:
                update_fields.append("issue_date = %s")
                params.append(bill.issue_date)
            if bill.terms_and_conditions is not None:
                update_fields.append("terms_and_conditions = %s")
                params.append(bill.terms_and_conditions)
            if bill.shipper_details is not None:
                update_fields.append("shipper_details = %s")
                params.append(bill.shipper_details)
            if bill.consignee_details is not None:
                update_fields.append("consignee_details = %s")
                params.append(bill.consignee_details)
            if bill.is_hazardous is not None:
                update_fields.append("is_hazardous = %s")
                params.append(bill.is_hazardous)

            if not update_fields:
                return await self.get_bill_of_lading_by_id(bill_id)

            update_fields.append("updated_at = NOW()")
            params.append(bill_id)

            query = f"UPDATE bills_of_lading SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_bill_of_lading_by_id(bill_id)
        except Exception as e:
            logging.error(f"Error updating bill of lading: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_bill_of_lading(self, bill_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM bills_of_lading WHERE id = %s"
            await self.db_service.execute(query, (bill_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting bill of lading: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()
