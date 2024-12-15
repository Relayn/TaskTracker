import unittest
import os
import json
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
    export_to_csv
)

class TestTaskTracker(unittest.TestCase):

    def setUp(self):
        global tasks
        tasks = []
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)

    def tearDown(self):
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)
        if os.path.exists("tasks.csv"):
            os.remove("tasks.csv")

    def test_save_and_load_tasks(self):
        global tasks
        tasks = [{"name": "Task 1", "priority": "Высокий", "completed": False}]
        save_tasks_to_file()
        loaded_tasks = load_tasks_from_file()
        self.assertEqual(loaded_tasks, tasks)

    def test_add_task(self):
        global tasks
        add_task()
        task_entry = unittest.mock.Mock()
        task_entry.get.return_value = "Task 1"
        priority_var = unittest.mock.Mock()
        priority_var.get.return_value = "Высокий"
        add_task()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["name"], "Task 1")
        self.assertEqual(tasks[0]["priority"], "Высокий")
        self.assertFalse(tasks[0]["completed"])

    def test_delete_task(self):
        global tasks
        tasks = [{"name": "Task 1", "priority": "Высокий", "completed": False}]
        delete_task()
        task_listBox = unittest.mock.Mock()
        task_listBox.curselection.return_value = (0,)
        delete_task()
        self.assertEqual(len(tasks), 0)

    def test_mark_task(self):
        global tasks
        tasks = [{"name": "Task 1", "priority": "Высокий", "completed": False}]
        mark_task()
        task_listBox = unittest.mock.Mock()
        task_listBox.curselection.return_value = (0,)
        mark_task()
        self.assertTrue(tasks[0]["completed"])

    def test_sort_tasks_by_priority(self):
        global tasks
        tasks = [
            {"name": "Task 1", "priority": "Средний", "completed": False},
            {"name": "Task 2", "priority": "Высокий", "completed": False},
            {"name": "Task 3", "priority": "Низкий", "completed": False}
        ]
        sort_tasks_by_priority()
        self.assertEqual(tasks[0]["priority"], "Высокий")
        self.assertEqual(tasks[1]["priority"], "Средний")
        self.assertEqual(tasks[2]["priority"], "Низкий")

    def test_export_to_csv(self):
        global tasks
        tasks = [{"name": "Task 1", "priority": "Высокий", "completed": False}]
        export_to_csv()
        with open("tasks.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()
            self.assertEqual(lines[0].strip(), "Имя задачи,Приоритет,Выполнено")
            self.assertEqual(lines[1].strip(), "Task 1,Высокий,Нет")

if __name__ == '__main__':
    unittest.main()
