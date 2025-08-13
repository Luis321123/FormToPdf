from fastapi import APIRouter

from app.api.endpoints.health_check import router as router_check    

api_router = APIRouter()

#route Checkout
api_router.include_router(router_check, tags=["HealthCheck"],
    responses={404: {"description": "Not found"}})



