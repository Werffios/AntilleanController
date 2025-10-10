from . import app

from fastapi import APIRouter

from app.routes import (
    customer_routes,
    location_routes,
    asset_routes,
    asset_type_routes,
    vessel_routes,
    route_routes,
    voyage_routes,
    shipment_routes,
    tracker_event_routes
)


api_router = APIRouter(prefix="/antillean/api")

# Register all routes
api_router.include_router(customer_routes.router)
api_router.include_router(location_routes.router)
api_router.include_router(asset_type_routes.router)
api_router.include_router(asset_routes.router)
api_router.include_router(vessel_routes.router)
api_router.include_router(route_routes.router)
api_router.include_router(voyage_routes.router)
api_router.include_router(shipment_routes.router)
api_router.include_router(tracker_event_routes.router)


app.include_router(api_router)