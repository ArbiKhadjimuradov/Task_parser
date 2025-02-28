import pytest
from src.models import Problem


def test_problem_model():
    """
    Проверяем, что модель Problem корректно создается.
    """
    problem = Problem(
        name="Test Problem",
        contest_id=1,
        rating=800,
    )
    assert problem.name == "Test Problem"
    assert problem.rating == 800
