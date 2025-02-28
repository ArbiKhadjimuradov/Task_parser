from src.db import init_db, SessionLocal
from src.models import Problem


def test_init_db(db_session):
    """
    Проверяем, что функция init_db корректно инициализирует базу данных.
    """
    init_db()
    assert db_session.query(Problem).count() == 0


def test_save_problem(db_session):
    """
    Проверяем, что задача корректно сохраняется в базу данных.
    """
    problem = Problem(
        name="Test Problem",
        contest_id=1,
        rating=800,
    )
    db_session.add(problem)
    db_session.commit()
    saved_problem = db_session.query(Problem).first()
    assert saved_problem.name == "Test Problem"
    assert saved_problem.rating == 800
