from dataclasses import dataclass

from .base import BaseController


@dataclass
class HealthCheckInput:
    pass


@dataclass
class HealthCheckOutput:
    status: str


class HealthCheckController(BaseController[HealthCheckInput, HealthCheckOutput]):
    def execute(self, input: HealthCheckInput) -> HealthCheckOutput:
        return HealthCheckOutput(status="OK")
