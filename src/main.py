import logging
import asyncio
import time
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.config import settings
from src.parser import CodeforcesParser
from src.bot.handlers import setup_bot
from src.db import init_db

logging.basicConfig(level=logging.INFO)


async def main():
    # Ждём, пока база данных будет готова
    time.sleep(10)  # Задержка 10 секунд

    # Инициализация базы данных
    init_db()

    # Инициализация бота
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    setup_bot(application)

    # Инициализация парсера
    parser = CodeforcesParser()

    # Планировщик для периодического парсинга
    scheduler = AsyncIOScheduler()
    scheduler.add_job(parser.parse_and_save, 'interval', hours=1)
    scheduler.start()

    # Запуск бота
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    try:
        # Бесконечный цикл для поддержания работы приложения
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        # Остановка бота и планировщика
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())