from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.config.scraper import SELENIUM_HOST, SELENIUM_PORT, SELENIUM_PROTOCOL

from dataclasses import dataclass
from datetime import datetime
import time
from typing import List, Optional


@dataclass
class RawReview:
    rating: float
    reviewer_name: str
    reviewer_country: Optional[str] = None
    review_date: Optional[datetime] = None
    content: Optional[str] = None
    negative: Optional[str] = None
    positive: Optional[str] = None


@dataclass
class ScrapeTarget:
    element: str = "div"
    class_name: Optional[str] = None


class ScaperService:
    review_blocks: ScrapeTarget
    reviewer_name: ScrapeTarget
    reviewer_country: ScrapeTarget
    review_date: ScrapeTarget
    rating: ScrapeTarget
    review_content: ScrapeTarget
    positive_review: ScrapeTarget
    negative_review: ScrapeTarget

    def __init__(self):
        # Setup Chrome
        self.options = Options()
        self.options.add_argument("--headless")  # run in background
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

    def _santize_date(self, date_str: str) -> datetime:
        """
        Convert the date string to a datetime object.
        This method should be implemented in subclasses.
        """
        return datetime.strptime(date_str, "%Y-%m-%d") if date_str else None

    def _find_element(self, soup: BeautifulSoup, target: ScrapeTarget) -> Optional[str]:
        if target.class_name:
            element = soup.find(target.element, class_=target.class_name)
        else:
            element = soup.find(target.element)

        if element:
            return element.get_text(strip=True)
        return None

    def _get_reviews(self, soup: BeautifulSoup) -> List[RawReview]:
        if not hasattr(self, 'review_blocks'):
            raise NotImplementedError(
                "This method should be implemented in subclasses.")

        review_blocks = soup.find_all(
            self.review_blocks.element,
            {'class': self.review_blocks.class_name}
        )

        reviews: List[RawReview] = []
        for block in review_blocks:
            reviewer_name = self._find_element(block, self.reviewer_name)
            reviewer_country = self._find_element(block, self.reviewer_country)
            review_date = self._find_element(block, self.review_date)
            rating = self._find_element(block, self.rating)
            review_content = self._find_element(block, self.review_content)
            positive_review = self._find_element(block, self.positive_review)
            negative_review = self._find_element(block, self.negative_review)

            reviews.append(RawReview(
                reviewer_name=reviewer_name,
                reviewer_country=reviewer_country,
                review_date=self._santize_date(review_date) if review_date else None,
                rating=float(rating) if rating else None,
                content=review_content,
                positive=positive_review,
                negative=negative_review
            ))

        return reviews

    def scrape(self, url: str) -> List[RawReview]:
        driver = webdriver.Remote(
            command_executor=f"{SELENIUM_PROTOCOL}://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
            options=self.options,
        )
        driver.get(url)
        time.sleep(10)  # Wait for the page to load

        # Scroll to the bottom of the page to load all reviews
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Parse the page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        try:
            reviews = self._get_reviews(soup)
            return reviews
        except Exception as e:
            raise e
        finally:
            # Ensure the driver is closed properly
            driver.quit()
