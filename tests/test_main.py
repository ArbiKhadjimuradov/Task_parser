import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from src.main import main


@pytest.mark.asyncio
async def test_main():
    # Создаем мок для Application и его билдера
    mock_app = AsyncMock()
    mock_builder = MagicMock()

    # Настраиваем цепочку вызовов: Application.builder().token().build()
    mock_builder.token.return_value = mock_builder
    mock_builder.build.return_value = mock_app

    # Эмулируем завершение run_polling
    mock_app.run_polling.side_effect = asyncio.CancelledError()

    # Мокируем init_db и setup_bot
    with patch("src.main.setup_bot") as mock_setup_bot, \
         patch("src.main.Application.builder", return_value=mock_builder), \
         patch("src.main.settings") as mock_settings:

        # Настраиваем мок для settings
        mock_settings.TELEGRAM_TOKEN = "test_token"


