from .base import router
from src.controllers.health_check import HealthCheckController, HealthCheckInput
from src.types.health import HealthCheckResponse


@router.get("/health", tags=["Health"], response_model=HealthCheckResponse, response_model_exclude_unset=True)
async def health_check():
    input = HealthCheckInput()
    controller = HealthCheckController()
    return controller.execute(input)
