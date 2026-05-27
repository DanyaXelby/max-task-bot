import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue
from dotenv import load_dotenv
from tasks import TaskManager

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

task_manager = TaskManager()

# Клавиатура для удобства
keyboard = [["Мои задачи", "Создать задачу"]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для управления задачами.\n"
        "Используйте кнопки ниже или команды:\n"
        "/tasks — показать мои задачи\n"
        "/newtask — создать новую задачу",
        reply_markup=reply_markup
    )

async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username
    tasks_text = task_manager.list_tasks(user)
    await update.message.reply_text(tasks_text)

async def create_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Формат создания задачи:\n"
        "`/task Название задачи | Описание | @ответственный | дней_до_срока`\n\n"
        "Пример:\n"
        "`/task Подготовить отчёт | Собрать данные за квартал | @ivanov | 3`",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith('/task'):
        try:
            parts = text[6:].split(' | ')
            if len(parts) != 4:
                await update.message.reply_text("Неверный формат. Используйте: /task ...")
                return

            title, description, assignee, days = parts
            days = int(days)
            result = task_manager.create_task(title, description, assignee, days)
            await update.message.reply_text(result)
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}")
    elif text == "Мои задачи":
        await show_tasks(update, context)
    elif text == "Создать задачу":
        await create_task_command(update, context)

def schedule_reminders(job_queue: JobQueue):
    job_queue.run_repeating(
        callback=check_deadlines_job,
        interval=3600,  # проверка каждый час
        first=10
    )

async def check_deadlines_job(context: ContextTypes.DEFAULT_TYPE):
    task_manager.check_deadlines(context)

def main():
    application = Application.builder().token(TOKEN).build()
    job_queue = application.job_queue

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tasks", show_tasks))
    application.add_handler(CommandHandler("newtask", create_task_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Расписание напоминаний
    schedule_reminders(job_queue)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
