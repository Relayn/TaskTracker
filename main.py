import tkinter as tk
from tkinter import messagebox
import json
import csv

# Файл для хранения задач
TASKS_FILE = 'tasks.json'

# Глобальный список задач
tasks = []


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===

# Функция обновляет список задач в графическом интерфейсе
def update_task_listbox():
    task_listBox.delete(0, tk.END)  # Очищаем список задач на экране
    for task in tasks:
        task_text = f"[{task['priority']}] {task['name']}"  # Формируем текст задачи
        task_listBox.insert(tk.END, task_text)  # Добавляем задачу в Listbox
        if task['completed']:  # Если задача выполнена, выделяем зеленым цветом
            task_listBox.itemconfig(tk.END, bg="light green")
    update_task_count()  # Обновляем счетчик задач


# Функция обновляет информацию о количестве задач
def update_task_count():
    total = len(tasks)  # Общее количество задач
    completed = sum(1 for task in tasks if task['completed'])  # Количество выполненных задач
    task_count_label.config(text=f"Всего задач: {total}, Выполнено: {completed}")


# Функция сохраняет задачи в файл в формате JSON
def save_tasks_to_file():
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)  # Сохраняем список задач в файл


# Функция загружает задачи из файла в формате JSON
def load_tasks_from_file():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)  # Загружаем список задач из файла
    except (FileNotFoundError, json.JSONDecodeError):  # Если файл не найден или поврежден
        return []  # Возвращаем пустой список задач


# === ФУНКЦИИ ДЛЯ РАБОТЫ С ЗАДАЧАМИ ===

# Функция добавляет новую задачу в список задач
def add_task():
    task_name = task_entry.get().strip()  # Получаем текст задачи из поля ввода
    if not task_name:  # Если текст пустой, показываем сообщение об ошибке
        messagebox.showwarning("Ошибка", "Введите задачу!")
        return
    tasks.append({
        "name": task_name,
        "priority": priority_var.get(),  # Приоритет задачи
        "completed": False  # Статус выполнения задачи
    })
    task_entry.delete(0, tk.END)  # Очищаем поле ввода
    save_tasks_to_file()  # Сохраняем задачи в файл
    update_task_listbox()  # Обновляем графический интерфейс


# Функция удаляет выбранную задачу из списка
def delete_task():
    selected_task_index = task_listBox.curselection()  # Получаем индекс выбранной задачи
    if not selected_task_index:  # Если ничего не выбрано, показываем сообщение об ошибке
        messagebox.showwarning("Ошибка", "Выберите задачу для удаления!")
        return
    tasks.pop(selected_task_index[0])  # Удаляем задачу из списка по индексу
    save_tasks_to_file()  # Сохраняем изменения в файл
    update_task_listbox()  # Обновляем графический интерфейс


# Функция отмечает выбранную задачу как выполненную
def mark_task():
    selected_task_index = task_listBox.curselection()  # Получаем индекс выбранной задачи
    if not selected_task_index:  # Если ничего не выбрано, показываем сообщение об ошибке
        messagebox.showwarning("Ошибка", "Выберите задачу для отметки!")
        return
    task = tasks[selected_task_index[0]]  # Получаем задачу по индексу
    if task['completed']:  # Если задача уже выполнена, показываем сообщение
        messagebox.showinfo("Информация", "Эта задача уже выполнена.")
    else:
        task['completed'] = True  # Отмечаем задачу как выполненную
        save_tasks_to_file()  # Сохраняем изменения в файл
        update_task_listbox()  # Обновляем графический интерфейс


# Функция сортирует задачи по приоритету
def sort_tasks_by_priority():
    global tasks
    priority_order = {"Высокий": 1, "Средний": 2, "Низкий": 3}  # Устанавливаем порядок приоритетов
    tasks.sort(key=lambda x: priority_order[x['priority']])  # Сортируем задачи по приоритету
    update_task_listbox()  # Обновляем графический интерфейс


# Функция экспортирует задачи в файл формата CSV
def export_to_csv():
    with open("tasks.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Имя задачи", "Приоритет", "Выполнено"])  # Заголовки столбцов
        for task in tasks:  # Перебираем задачи и записываем их в файл
            writer.writerow([task['name'], task['priority'], "Да" if task['completed'] else "Нет"])
    messagebox.showinfo("Успех", "Задачи экспортированы в tasks.csv")  # Сообщение об успешном экспорте


# === НАСТРОЙКА ГРАФИЧЕСКОГО ИНТЕРФЕЙСА ===

# Создаем главное окно
root = tk.Tk()
root.title("Список задач")  # Устанавливаем заголовок окна
root.configure(background="light blue")  # Устанавливаем цвет фона

# Создаем поле для ввода задачи
tk.Label(root, text="Введите вашу задачу:", bg="light blue").pack(pady=5)
task_entry = tk.Entry(root, width=30)  # Поле для текста задачи
task_entry.pack(pady=5)

# Создаем меню выбора приоритета задачи
priority_var = tk.StringVar(value="Средний")  # Устанавливаем приоритет по умолчанию
tk.Label(root, text="Приоритет:", bg="light blue").pack(pady=5)
tk.OptionMenu(root, priority_var, "Высокий", "Средний", "Низкий").pack(pady=5)

# Создаем кнопки для управления задачами
tk.Button(root, text="Добавить задачу", command=add_task).pack(pady=5)  # Кнопка "Добавить задачу"
tk.Button(root, text="Удалить задачу", command=delete_task).pack(pady=5)  # Кнопка "Удалить задачу"
tk.Button(root, text="Отметить выполненную задачу", command=mark_task).pack(pady=5)  # Кнопка "Отметить выполненную"
tk.Button(root, text="Сортировать по приоритету", command=sort_tasks_by_priority).pack(pady=5)  # Кнопка "Сортировать"
tk.Button(root, text="Экспортировать в CSV", command=export_to_csv).pack(pady=5)  # Кнопка "Экспортировать в CSV"

# Создаем список задач
tk.Label(root, text="Список задач:", bg="light blue").pack(pady=5)
task_listBox = tk.Listbox(root, height=10, width=50)  # Поле для отображения задач
task_listBox.pack(pady=10)

# Создаем метку для отображения количества задач
task_count_label = tk.Label(root, text="Всего задач: 0, Выполнено: 0", bg="light blue")
task_count_label.pack(pady=5)

# Загружаем задачи из файла при запуске приложения
tasks = load_tasks_from_file()  # Загружаем задачи из файла
update_task_listbox()  # Отображаем задачи в интерфейсе

# Запускаем главный цикл обработки событий
root.mainloop()
