import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update
from telegram.ext import CallbackContext
from src.bot.handlers import start, handle_rating


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


@pytest.mark.asyncio
async def test_start(mock_update, mock_context):
    """
    Проверяем, что команда /start отправляет приветственное сообщение.
    """
    await start(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with(
        "Привет! Я бот для поиска задач с Codeforces.\n"
        "Введите сложность задачи (например, 800) или сложность и лимит (например, 800 5):"
    )


@pytest.mark.asyncio
async def test_handle_rating_invalid_input(mock_update, mock_context):
    """
    Проверяем, что бот корректно обрабатывает некорректный ввод.
    """
    mock_update.message.text = "invalid"
    await handle_rating(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with(
        "Пожалуйста, введите сложность задачи (например, 800) или сложность и лимит (например, 800 5)."
    )


@pytest.mark.asyncio
async def test_handle_rating_valid_input_with_limit(mock_update, mock_context):
    """
    Проверяем обработку валидного ввода с указанием лимита задач.
    """
    # Устанавливаем входные данные
    mock_update.message.text = "800 5"

    # Замокаем ответ парсера
    mock_problems = [
        {"name": "Problem 1", "rating": 800, "contestId": 1, "index": "A", "tags": ["math"]},
        {"name": "Problem 2", "rating": 800, "contestId": 2, "index": "B", "tags": ["greedy"]}
    ]

    with patch("src.parser.CodeforcesParser.get_problem", return_value=mock_problems):
        await handle_rating(mock_update, mock_context)

        # Проверяем вызовы
        mock_update.message.reply_text.assert_called()

        # Получаем аргументы последнего вызова reply_text
        args, _ = mock_update.message.reply_text.call_args
        response = args[0]

        # Проверяем содержание ответа
        assert "Problem 1" in response
        assert "Problem 2" in response
        assert "math" in response
        assert "greedy" in response


@pytest.mark.asyncio
async def test_handle_rating_no_problems(mock_update, mock_context):
    mock_update.message.text = "800"
    with patch("src.parser.CodeforcesParser.get_problem", return_value=[]):
        await handle_rating(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_with("Задачи с такой сложностью не найдены.")