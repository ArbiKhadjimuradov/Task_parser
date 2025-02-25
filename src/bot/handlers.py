from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.services.problem_service import ProblemService
from src.db import SessionLocal


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для поиска задач с Codeforces.\n"
        "Введите сложность задачи (например, 800):"
    )


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rating = update.message.text
    if rating.isdigit():
        await update.message.reply_text(f"Вы выбрали сложность: {rating}. Ищу задачи...")

        # Поиск задач по сложности
        db = SessionLocal()
        try:
            problem_service = ProblemService(db)
            problems = problem_service.get_problems_by_filter(rating=int(rating))
            if problems:
                response = "\n".join([f"{p.name} (сложность: {p.rating})" for p in problems])
                await update.message.reply_text(f"Найдены задачи:\n{response}")
            else:
                await update.message.reply_text("Задачи с такой сложностью не найдены.")
        finally:
            db.close()
    else:
        await update.message.reply_text("Пожалуйста, введите число (например, 800).")


def setup_bot(app: Application):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_rating))