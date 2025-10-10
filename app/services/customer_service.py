import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.customer_models import CustomerCreate, CustomerUpdate, CustomerResponse


class CustomerService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_customer(self, customer: CustomerCreate) -> CustomerResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO customers (full_name, identification_number, email, phone_number, created_at, updated_at)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
            """
            params = (customer.full_name, customer.identification_number, customer.email, customer.phone_number)
            await self.db_service.execute(query, params)

            # Get the created customer
            select_query = "SELECT * FROM customers WHERE identification_number = %s"
            result = await self.db_service.execute(select_query, (customer.identification_number,))

            if result:
                return CustomerResponse(**result[0])
            raise ValueError("Customer creation failed")
        except Exception as e:
            logging.error(f"Error creating customer: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_customer_by_id(self, customer_id: int) -> Optional[CustomerResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM customers WHERE id = %s"
            result = await self.db_service.execute(query, (customer_id,))

            if result:
                return CustomerResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving customer: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_customers(self, limit: int = 100, offset: int = 0) -> List[CustomerResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM customers LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [CustomerResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving customers: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_customer(self, customer_id: int, customer: CustomerUpdate) -> Optional[CustomerResponse]:
        try:
            await self.db_service.connect()

            # Build dynamic update query
            update_fields = []
            params = []

            if customer.full_name is not None:
                update_fields.append("full_name = %s")
                params.append(customer.full_name)
            if customer.identification_number is not None:
                update_fields.append("identification_number = %s")
                params.append(customer.identification_number)
            if customer.email is not None:
                update_fields.append("email = %s")
                params.append(customer.email)
            if customer.phone_number is not None:
                update_fields.append("phone_number = %s")
                params.append(customer.phone_number)

            if not update_fields:
                return await self.get_customer_by_id(customer_id)

            update_fields.append("updated_at = NOW()")
            params.append(customer_id)

            query = f"UPDATE customers SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_customer_by_id(customer_id)
        except Exception as e:
            logging.error(f"Error updating customer: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_customer(self, customer_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM customers WHERE id = %s"
            await self.db_service.execute(query, (customer_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting customer: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

