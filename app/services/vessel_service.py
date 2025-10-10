import logging
from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models.vessel_models import VesselCreate, VesselUpdate, VesselResponse


class VesselService:
    def __init__(self):
        self.db_service = DatabaseService()

    async def create_vessel(self, vessel: VesselCreate) -> VesselResponse:
        try:
            await self.db_service.connect()
            query = """
                INSERT INTO vessels (vessel_name, imo_number, mmsi_number, call_sign, ais_transponder_class,
                                    general_vessel_type, detailed_vessel_type, service_status, port_of_registry,
                                    year_built, dimensions, design_description, last_dry_dock_survey,
                                    tonnage_info, engine_info, capacity_info, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (
                vessel.vessel_name, vessel.imo_number, vessel.mmsi_number, vessel.call_sign,
                vessel.ais_transponder_class, vessel.general_vessel_type, vessel.detailed_vessel_type,
                vessel.service_status, vessel.port_of_registry, vessel.year_built, vessel.dimensions,
                vessel.design_description, vessel.last_dry_dock_survey, vessel.tonnage_info,
                vessel.engine_info, vessel.capacity_info
            )
            await self.db_service.execute(query, params)

            select_query = "SELECT * FROM vessels WHERE imo_number = %s"
            result = await self.db_service.execute(select_query, (vessel.imo_number,))

            if result:
                return VesselResponse(**result[0])
            raise ValueError("Vessel creation failed")
        except Exception as e:
            logging.error(f"Error creating vessel: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_vessel_by_id(self, vessel_id: int) -> Optional[VesselResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM vessels WHERE id = %s"
            result = await self.db_service.execute(query, (vessel_id,))

            if result:
                return VesselResponse(**result[0])
            return None
        except Exception as e:
            logging.error(f"Error retrieving vessel: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def get_all_vessels(self, limit: int = 100, offset: int = 0) -> List[VesselResponse]:
        try:
            await self.db_service.connect()
            query = "SELECT * FROM vessels LIMIT %s OFFSET %s"
            result = await self.db_service.execute(query, (limit, offset))

            return [VesselResponse(**row) for row in result]
        except Exception as e:
            logging.error(f"Error retrieving vessels: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def update_vessel(self, vessel_id: int, vessel: VesselUpdate) -> Optional[VesselResponse]:
        try:
            await self.db_service.connect()

            update_fields = []
            params = []

            if vessel.vessel_name is not None:
                update_fields.append("vessel_name = %s")
                params.append(vessel.vessel_name)
            if vessel.imo_number is not None:
                update_fields.append("imo_number = %s")
                params.append(vessel.imo_number)
            if vessel.mmsi_number is not None:
                update_fields.append("mmsi_number = %s")
                params.append(vessel.mmsi_number)
            if vessel.call_sign is not None:
                update_fields.append("call_sign = %s")
                params.append(vessel.call_sign)
            if vessel.ais_transponder_class is not None:
                update_fields.append("ais_transponder_class = %s")
                params.append(vessel.ais_transponder_class)
            if vessel.general_vessel_type is not None:
                update_fields.append("general_vessel_type = %s")
                params.append(vessel.general_vessel_type)
            if vessel.detailed_vessel_type is not None:
                update_fields.append("detailed_vessel_type = %s")
                params.append(vessel.detailed_vessel_type)
            if vessel.service_status is not None:
                update_fields.append("service_status = %s")
                params.append(vessel.service_status)
            if vessel.port_of_registry is not None:
                update_fields.append("port_of_registry = %s")
                params.append(vessel.port_of_registry)
            if vessel.year_built is not None:
                update_fields.append("year_built = %s")
                params.append(vessel.year_built)
            if vessel.dimensions is not None:
                update_fields.append("dimensions = %s")
                params.append(vessel.dimensions)
            if vessel.design_description is not None:
                update_fields.append("design_description = %s")
                params.append(vessel.design_description)
            if vessel.last_dry_dock_survey is not None:
                update_fields.append("last_dry_dock_survey = %s")
                params.append(vessel.last_dry_dock_survey)
            if vessel.tonnage_info is not None:
                update_fields.append("tonnage_info = %s")
                params.append(vessel.tonnage_info)
            if vessel.engine_info is not None:
                update_fields.append("engine_info = %s")
                params.append(vessel.engine_info)
            if vessel.capacity_info is not None:
                update_fields.append("capacity_info = %s")
                params.append(vessel.capacity_info)

            if not update_fields:
                return await self.get_vessel_by_id(vessel_id)

            update_fields.append("updated_at = NOW()")
            params.append(vessel_id)

            query = f"UPDATE vessels SET {', '.join(update_fields)} WHERE id = %s"
            await self.db_service.execute(query, tuple(params))

            return await self.get_vessel_by_id(vessel_id)
        except Exception as e:
            logging.error(f"Error updating vessel: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

    async def delete_vessel(self, vessel_id: int) -> bool:
        try:
            await self.db_service.connect()
            query = "DELETE FROM vessels WHERE id = %s"
            await self.db_service.execute(query, (vessel_id,))
            return True
        except Exception as e:
            logging.error(f"Error deleting vessel: {str(e)}")
            raise
        finally:
            await self.db_service.disconnect()

