from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.services.problem_service import ProblemService
from src.db import SessionLocal
from src.parser import CodeforcesParser


def split_text(text, max_length=4096):
    """
    Разбивает текст на части, каждая из которых не превышает max_length символов.
    """
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для поиска задач с Codeforces.\n"
        "Введите сложность задачи (например, 800) или сложность и лимит (например, 800 5):"
    )


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.split()
    if len(text) == 1 and text[0].isdigit():
        # Если пользователь ввел только сложность (например, "800")
        rating = int(text[0])
        limit = 10  # Значение по умолчанию
    elif len(text) == 2 and text[0].isdigit() and text[1].isdigit():
        # Если пользователь ввел сложность и лимит (например, "800 5")
        rating = int(text[0])
        limit = int(text[1])
    else:
        await update.message.reply_text(
            "Пожалуйста, введите сложность задачи (например, 800) или сложность и лимит (например, 800 5)."
        )
        return

    await update.message.reply_text(f"Вы выбрали сложность: {rating}. Ищу задачи...")

    # Получаем задачи с Codeforces
    parser = CodeforcesParser()
    problems = parser.get_problem(difficulty=rating)
    if problems:
        # Ограничиваем количество задач
        problems = problems[:limit]

        # Формируем сообщение с задачами
        response = "\n\n".join(
            [
                f"Название: {p['name']}\n"
                f"Сложность: {p.get('rating', 'Не указана')}\n"
                f"Ссылка: https://codeforces.com/problemset/problem/{p['contestId']}/{p['index']}\n"
                f"Теги: {', '.join(p['tags'])}"
                for p in problems
            ]
        )

        # Разбиваем сообщение на части
        for part in split_text(response):
            await update.message.reply_text(part)
    else:
        await update.message.reply_text("Задачи с такой сложностью не найдены.")


def setup_bot(app: Application):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_rating))