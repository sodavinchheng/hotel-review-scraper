from fastapi import Request

from src.config.scraper import WebsiteType
from src.services.scraper import ScaperService
from src.services.booking_dot_com import BookingDotComService
from src.services.trip_advisor import TripAdvisorService


def get_scraper(request: Request) -> ScaperService:
    type = request.query_params.get("type", None)
    if type is None:
        # check request body if type is not in query params
        body = request.json()
        type = body.get("type", WebsiteType.OTHER.value)

    if type == str(WebsiteType.BOOKING.value):
        return BookingDotComService()
    elif type == str(WebsiteType.TRIPADVISOR.value):
        return TripAdvisorService()
    else:
        raise ValueError(f"Unknown scraper type: {type}")
