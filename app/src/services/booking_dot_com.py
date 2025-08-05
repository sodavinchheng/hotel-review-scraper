from datetime import datetime

from .scraper import ScaperService, ScrapeTarget


class BookingDotComService(ScaperService):
    def __init__(self, ):
        super().__init__()
        self.review_blocks = ScrapeTarget(element="li", class_name="review_item")
        self.reviewer_name = ScrapeTarget(element="p", class_name="reviewer_name")
        self.reviewer_country = ScrapeTarget(element="span", class_name="reviewer_country")
        self.review_date = ScrapeTarget(element="p", class_name="review_item_date")
        self.rating = ScrapeTarget(element="span", class_name="review-score-badge")
        self.review_content = ScrapeTarget(element="div", class_name="review_item_header_content")
        self.positive_review = ScrapeTarget(element="p", class_name="review_pos")
        self.negative_review = ScrapeTarget(element="p", class_name="review_neg")

    def _santize_date(self, date_str: str) -> datetime:
        """
        Convert the date string from Booking.com to a datetime object.
        The date format is typically "投稿日：2025年3月31日" if Japanese.
        If English, the format is "Reviewed: July 13, 2025"
        """
        try:
            date_str = date_str.replace("投稿日：", "").replace("年", "-").replace("月", "-").replace("日", "")
            return datetime.strptime(date_str, "%Y-%m-%d") if date_str else None
        except ValueError:
            # If the Japanese format fails, try the English format
            try:
                return datetime.strptime(date_str, "Reviewed: %B %d, %Y")
            except ValueError:
                return None
        
