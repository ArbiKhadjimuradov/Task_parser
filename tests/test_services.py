from src.models import Problem
from src.services.problem_service import ProblemService


def test_problem_service_get_problems(db_session):
    """
    Проверяем, что ProblemService корректно возвращает задачи.
    """
    problem = Problem(
        name="Test Problem",
        contest_id=1,
        rating=800,
    )
    db_session.add(problem)
    db_session.commit()

    service = ProblemService(db_session)
    problems = service.get_problems_by_filter(rating=800)
    assert len(problems) == 1
    assert problems[0].name == "Test Problem"