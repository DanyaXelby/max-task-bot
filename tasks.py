from datetime import datetime, timedelta
from database import TaskDatabase

class TaskManager:
    def __init__(self):
        self.db = TaskDatabase()

    def create_task(self, title, description, assignee, days_to_deadline):
        deadline = (datetime.now() + timedelta(days=days_to_deadline)).isoformat()
        self.db.add_task(title, description, assignee, deadline)
        return f"Задача '{title}' создана для {assignee}. Срок: {deadline[:16]}"

    def list_tasks(self, user):
        tasks = self.db.get_tasks_by_assignee(user)
        if not tasks:
            return "У вас нет активных задач."

        result = "Ваши активные задачи:\n"
        for task in tasks:
            result += f"• {task[1]} (до {task[4][:16]})\n"
        return result

    def check_deadlines(self, context):
        overdue = self.db.get_overdue_tasks()
        for task in overdue:
            context.bot.send_message(
                chat_id=task[3],  # предполагаем, что assignee — это ID чата
                text=f"⚠️ Напоминание: задача '{task[1]}' просрочена!"
            )
