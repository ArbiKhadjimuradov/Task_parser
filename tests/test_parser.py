import requests
import pytest
from src.parser import CodeforcesParser
from unittest.mock import patch, MagicMock


def test_get_problem_with_difficulty():
    """
    Проверяем, что функция get_problem возвращает задачи с указанной сложностью.
    """
    parser = CodeforcesParser()
    problems = parser.get_problem(difficulty=800)
    assert problems is not None
    assert len(problems) > 0
    for problem in problems:
        assert problem.get("rating") == 800


def test_get_problem_without_difficulty():
    """
    Проверяем, что функция get_problem возвращает все задачи, если сложность не указана.
    """
    parser = CodeforcesParser()
    problems = parser.get_problem()
    assert problems is not None
    assert len(problems) > 0


def test_get_problem_invalid_difficulty():
    """
    Проверяем, что функция get_problem возвращает пустой список, если задачи с указанной сложностью не найдены.
    """
    parser = CodeforcesParser()
    problems = parser.get_problem(difficulty=999999)
    assert problems == []


def test_get_problem_api_error():
    """
    Проверяем, что функция get_problem возвращает None, если API возвращает ошибку.
    """
    parser = CodeforcesParser()
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500  # Симулируем ошибку сервера
        problems = parser.get_problem()
        assert problems is None


def test_get_problem_api_status_not_ok():
    """
    Проверяем, что функция get_problem возвращает None, если статус ответа не "OK".
    """
    parser = CodeforcesParser()
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"status": "FAILED"}  # Симулируем статус не "OK"
        problems = parser.get_problem()
        assert problems is None


def test_get_problem_timeout():
    """
    Проверяем, что функция get_problem возвращает None, если возникает таймаут.
    """
    parser = CodeforcesParser()
    with patch("requests.get", side_effect=requests.Timeout):
        problems = parser.get_problem()
        assert problems is None