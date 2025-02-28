import requests
import pytest
from src.parser import CodeforcesParser


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
