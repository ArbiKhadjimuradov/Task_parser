import pytest
from unittest.mock import patch, Mock
from app.models import Problem
from app.parser import CodeforcesParser


@patch('requests.get')
def test_parser(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        'result': {
            'problems': [{'contestId': 1, 'index': 'A', 'name': 'Test', 'tags': ['math'], 'rating': 800}],
            'problemStatistics': [{'solvedCount': 100}]
        }
    }
    mock_get.return_value = mock_response

    parser = CodeforcesParser()
    parser.parse_and_save()

    # Проверка сохранения в БД
    db = SessionLocal()
    problem = db.query(Problem).first()
    assert problem.name == 'Test'
    assert problem.rating == 800
    db.close()
