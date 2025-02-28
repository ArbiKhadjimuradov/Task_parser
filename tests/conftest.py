import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db import Base
from src.models import Problem
from telegram import Update
from telegram.ext import CallbackContext
from unittest.mock import AsyncMock


@pytest.fixture
def db_session():
    """
    Фикстура для создания тестовой сессии базы данных.
    """
    # Создаем базу данных в памяти (SQLite)
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)  # Создаем таблицы
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # Возвращаем сессию для использования в тестах
    session.close()  # Закрываем сессию после завершения теста


@pytest.fixture
def test_problem(db_session):
    """
    Фикстура для создания тестовой задачи в базе данных.
    """
    problem = Problem(
        name="Test Problem",
        contest_id=1,
        index="A",
        rating=800,
        tags="test, example"
    )
    db_session.add(problem)
    db_session.commit()
    return problem


@pytest.fixture
def mock_update():
    """
    Фикстура для создания мока Update.
    """
    update = AsyncMock(spec=Update)
    update.update_id = 123  # Указываем update_id
    update.message = AsyncMock()
    update.message.text = "800"
    return update


@pytest.fixture
def mock_context():
    """
    Фикстура для создания мока Context.
    """
    return AsyncMock(spec=CallbackContext)

