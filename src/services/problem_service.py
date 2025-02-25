import logging
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List, Optional
from ..models import Problem, Tag

logger = logging.getLogger(__name__)


class ProblemService:
    def __init__(self, db: Session):
        self.db = db

    def get_problems_by_filter(
            self,
            rating: Optional[int] = None,
            tag: Optional[str] = None,
            limit: int = 10
    ) -> List[Problem]:
        query = self.db.query(Problem)

        if rating:
            logger.info(f"Filtering problems by rating: {rating}")
            query = query.filter(Problem.rating == rating)
        if tag:
            logger.info(f"Filtering problems by tag: {tag}")
            query = query.join(Problem.tags).filter(Tag.name == tag)

        # Получаем уникальные контесты
        subquery = (
            query.with_entities(Problem.contest_id)
            .distinct()
            .limit(limit)
            .subquery()
        )

        problems = (
            self.db.query(Problem)
            .join(subquery, Problem.contest_id == subquery.c.contest_id)
            .limit(limit)
            .all()
        )

        logger.info(f"Found {len(problems)} problems")
        return problems