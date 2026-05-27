// script.js
function sendTaskToBot() {
  const taskTitle = document.getElementById('taskInput').value;
  const deadline = document.getElementById('dateInput').value;

  // Отправляем данные в бот через MAX Bridge
  if (window.max) {
    max.send({
      action: 'create_task',
      data: {
        title: taskTitle,
        deadline: deadline,
        assignee: '@current_user' // или получите из контекста
      }
    });
  } else {
    alert('MAX Bridge недоступен');
  }
}
