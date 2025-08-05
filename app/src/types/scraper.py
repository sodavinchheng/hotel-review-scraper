from enum import Enum


class WebsiteType(Enum):
    BOOKING = 1
    TRIPADVISOR = 2
    OTHER = 999

    def __str__(self):
        return self.value
