import unittest
import os
import json
import sys
import tkinter as tk

# Добавляем родительскую директорию в sys.path, чтобы main.py был доступен для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch, MagicMock
from main import (
    TASKS_FILE,
    tasks,
    update_task_listbox,
    update_task_count,
    save_tasks_to_file,
    load_tasks_from_file,
    add_task,
    delete_task,
    mark_task,
    sort_tasks_by_priority,
    export_to_csv,
)


class TestTaskTracker(unittest.TestCase):

    def setUp(self):
        global tasks
        tasks.clear()
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)

        self.patcher_task_entry = patch("main.task_entry")
        self.mock_task_entry = self.patcher_task_entry.start()
        self.mock_task_entry.get.return_value = "Mocked Task"

        self.patcher_priority_var = patch("main.priority_var")
        self.mock_priority_var = self.patcher_priority_var.start()
        self.mock_priority_var.get.return_value = "Средний"

        self.patcher_task_listBox = patch("main.task_listBox")
        self.mock_task_listBox = self.patcher_task_listBox.start()
        self.mock_task_listBox.curselection.return_value = (0,)

        self.patcher_task_count_label = patch("main.task_count_label")
        self.mock_task_count_label = self.patcher_task_count_label.start()

        self.patcher_messagebox = patch("main.messagebox")
        self.mock_messagebox = self.patcher_messagebox.start()

        self.patcher_update_task_listbox = patch("main.update_task_listbox")
        self.mock_update_task_listbox = self.patcher_update_task_listbox.start()

        self.patcher_update_task_count = patch("main.update_task_count")
        self.mock_update_task_count = self.patcher_update_task_count.start()

    def tearDown(self):
        self.patcher_task_entry.stop()
        self.patcher_priority_var.stop()
        self.patcher_task_listBox.stop()
        self.patcher_task_count_label.stop()
        self.patcher_messagebox.stop()
        self.patcher_update_task_listbox.stop()
        self.patcher_update_task_count.stop()
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)
        if os.path.exists("tasks.csv"):
            os.remove("tasks.csv")

    def test_save_and_load_tasks(self):
        global tasks
        tasks.append({"name": "Task 1", "priority": "Высокий", "completed": False})
        save_tasks_to_file()
        loaded_tasks = load_tasks_from_file()
        self.assertEqual(loaded_tasks, tasks)
        self.assertTrue(os.path.exists(TASKS_FILE))
        with open(TASKS_FILE, "r") as f:
            content = json.load(f)
            self.assertEqual(content, tasks)

    def test_add_task(self):
        global tasks
        self.mock_task_entry.get.return_value = "New Task"
        self.mock_priority_var.get.return_value = "Высокий"

        add_task()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["name"], "New Task")
        self.assertEqual(tasks[0]["priority"], "Высокий")
        self.assertFalse(tasks[0]["completed"])
        self.mock_task_entry.delete.assert_called_once_with(0, tk.END)
        self.mock_update_task_listbox.assert_called_once()
        saved_tasks = load_tasks_from_file()
        self.assertEqual(saved_tasks, tasks)

        self.mock_task_entry.get.return_value = ""
        self.mock_messagebox.showwarning.reset_mock()
        add_task()
        self.assertEqual(len(tasks), 1)
        self.mock_messagebox.showwarning.assert_called_once_with(
            "Ошибка", "Введите задачу!"
        )

    def test_delete_task(self):
        global tasks
        tasks.append({"name": "Task 1", "priority": "Высокий", "completed": False})
        tasks.append({"name": "Task 2", "priority": "Средний", "completed": False})

        self.mock_task_listBox.curselection.return_value = (0,)
        delete_task()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["name"], "Task 2")
        self.mock_update_task_listbox.assert_called_once()
        saved_tasks = load_tasks_from_file()
        self.assertEqual(saved_tasks, tasks)

        self.mock_task_listBox.curselection.return_value = ()
        self.mock_messagebox.showwarning.reset_mock()
        delete_task()
        self.assertEqual(len(tasks), 1)
        self.mock_messagebox.showwarning.assert_called_once_with(
            "Ошибка", "Выберите задачу для удаления!"
        )

    def test_mark_task(self):
        global tasks
        tasks.append({"name": "Task 1", "priority": "Высокий", "completed": False})

        self.mock_task_listBox.curselection.return_value = (0,)
        mark_task()

        self.assertTrue(tasks[0]["completed"])
        self.mock_update_task_listbox.assert_called_once()
        saved_tasks = load_tasks_from_file()
        self.assertEqual(saved_tasks, tasks)

        self.mock_update_task_listbox.reset_mock()
        self.mock_messagebox.showinfo.reset_mock()
        mark_task()
        self.mock_messagebox.showinfo.assert_called_once_with(
            "Информация", "Эта задача уже выполнена."
        )
        self.mock_update_task_listbox.assert_not_called()

        tasks.clear()
        tasks.append(
            {"name": "Task to not mark", "priority": "Низкий", "completed": False}
        )
        self.mock_task_listBox.curselection.return_value = ()
        self.mock_messagebox.showwarning.reset_mock()
        mark_task()
        self.assertFalse(tasks[0]["completed"])
        self.mock_messagebox.showwarning.assert_called_once_with(
            "Ошибка", "Выберите задачу для отметки!"
        )

    def test_sort_tasks_by_priority(self):
        global tasks
        tasks.extend(
            [
                {"name": "Task 1", "priority": "Средний", "completed": False},
                {"name": "Task 2", "priority": "Высокий", "completed": False},
                {"name": "Task 3", "priority": "Низкий", "completed": False},
            ]
        )
        sort_tasks_by_priority()
        self.assertEqual(tasks[0]["priority"], "Высокий")
        self.assertEqual(tasks[1]["priority"], "Средний")
        self.assertEqual(tasks[2]["priority"], "Низкий")
        self.mock_update_task_listbox.assert_called_once()

    def test_export_to_csv(self):
        global tasks
        tasks.append({"name": "Task 1", "priority": "Высокий", "completed": False})
        tasks.append(
            {"name": "2 Completed Task", "priority": "Низкий", "completed": True}
        )

        export_to_csv()

        self.assertTrue(os.path.exists("tasks.csv"))
        with open("tasks.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()
            self.assertEqual(lines[0].strip(), "Имя задачи,Приоритет,Выполнено")
            self.assertEqual(lines[1].strip(), "Task 1,Высокий,Нет")
            self.assertEqual(lines[2].strip(), "2 Completed Task,Низкий,Да")
        self.mock_messagebox.showinfo.assert_called_once_with(
            "Успех", "Задачи экспортированы в tasks.csv"
        )


if __name__ == "__main__":
    unittest.main()
