from sqlalchemy import text
from sqlalchemy.orm import Query, Session


class BaseRepository:
    class InvalidIdError(Exception):
        pass

    def __init__(self, session: Session) -> None:
        self.session = session

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def begin_transaction(self):
        return self.session.begin_nested()

    def apply_sort(self, query: Query, sort_key: str, sort_order: str) -> Query:
        """
        Apply sorting to the given SQLAlchemy query based on the provided sort key and sort order.

        Args:
            query (Query): The SQLAlchemy query object to which sorting will be applied.
            sort_key (str): The column name to sort by. If not fully qualified, the table name will be prefixed.
            sort_order (str): The order of sorting, either 'asc' for ascending or 'desc' for descending.

        Returns:
            Query: The SQLAlchemy query object with the applied sorting.
        """
        table = query.column_descriptions[0]["entity"].__tablename__
        # If column is not fully qualified, add table name
        if len(sort_key.split(".")) < 2:
            sort_key = f"{table}.{sort_key}"
        return query.order_by(text(f"{sort_key} {sort_order.upper()}"))

    def apply_pagination(self, query: Query, page: int, page_size: int) -> Query:
        """
        Apply pagination to a SQLAlchemy query.

        This method modifies the given SQLAlchemy query to include pagination
        based on the specified page number and page size.

        Args:
            query (Query): The SQLAlchemy query to which pagination will be applied.
            page (int): The current page number (1-based index).
            page_size (int): The number of items per page.

        Returns:
            Query: The modified SQLAlchemy query with pagination applied.
        """
        return query.limit(page_size).offset((page - 1) * page_size)
