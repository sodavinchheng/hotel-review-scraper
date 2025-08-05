from enum import Enum
import os


SELENIUM_PROTOCOL = os.getenv('SELENIUM_PROTOCOL', 'http')
SELENIUM_HOST = os.getenv('SELENIUM_HOST', 'selenium')
SELENIUM_PORT = os.getenv('SELENIUM_PORT', '4444')

class WebsiteType(Enum):
    BOOKING = 1
    TRIPADVISOR = 2
    OTHER = 999

    def __str__(self):
        return self.value
