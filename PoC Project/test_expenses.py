import os
import json
import tempfile
import unittest

from expense_manager import ExpenseManager
from storage import Storage


def make_temp_json():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    return path


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.filepath = make_temp_json()

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_load_missing_file(self):
        os.unlink(self.filepath)
        s = Storage(self.filepath)
        self.assertEqual(s.load(), [])

    def test_load_empty_file(self):
        s = Storage(self.filepath)
        self.assertEqual(s.load(), [])

    def test_save_and_load(self):
        data = [{"id": "1", "amount": 10.0}]
        s = Storage(self.filepath)
        s.save(data)
        self.assertEqual(s.load(), data)


class TestExpenseManager(unittest.TestCase):
    def setUp(self):
        self.filepath = make_temp_json()
        self.manager = ExpenseManager(self.filepath)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_add_expense(self):
        expense = self.manager.add_expense(25.50, "Lunch", "food")
        self.assertEqual(expense["amount"], 25.50)
        self.assertEqual(expense["description"], "Lunch")
        self.assertEqual(expense["category"], "food")
        self.assertIn("id", expense)

    def test_add_expense_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(-10, "Bad", "food")

    def test_add_expense_rejects_zero(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(0, "Bad", "food")

    def test_add_expense_rejects_non_numeric(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense("abc", "Bad", "food")

    def test_list_expenses(self):
        self.manager.add_expense(10, "Coffee", "food")
        self.manager.add_expense(50, "Gas", "transport")
        self.assertEqual(len(self.manager.list_expenses()), 2)

    def test_list_filter_category(self):
        self.manager.add_expense(10, "Coffee", "food")
        self.manager.add_expense(50, "Gas", "transport")
        food = self.manager.list_expenses(category="food")
        self.assertEqual(len(food), 1)
        self.assertEqual(food[0]["description"], "Coffee")

    def test_list_filter_category_normalized(self):
        self.manager.add_expense(10, "Coffee", "Food")
        food = self.manager.list_expenses(category=" FOOD ")
        self.assertEqual(len(food), 1)
        self.assertEqual(food[0]["description"], "Coffee")

    def test_total(self):
        self.manager.add_expense(10, "A", "food")
        self.manager.add_expense(20, "B", "food")
        self.assertEqual(self.manager.total(), 30)

    def test_total_by_category(self):
        self.manager.add_expense(10, "A", "food")
        self.manager.add_expense(20, "B", "transport")
        self.assertEqual(self.manager.total(category="food"), 10)

    def test_delete_expense(self):
        expense = self.manager.add_expense(10, "Coffee", "food")
        expense_id = expense["id"]
        self.assertEqual(len(self.manager.list_expenses()), 1)
        self.manager.delete_expense(expense_id)
        self.assertEqual(len(self.manager.list_expenses()), 0)

    def test_delete_expense_not_found(self):
        with self.assertRaises(ValueError):
            self.manager.delete_expense("nonexistent-id")

    def test_delete_expense_updates_storage(self):
        expense = self.manager.add_expense(25.0, "Lunch", "food")
        expense_id = expense["id"]
        self.manager.delete_expense(expense_id)
        remaining = self.manager.list_expenses()
        self.assertEqual(len(remaining), 0)
        self.assertNotIn(expense_id, [e["id"] for e in remaining])

    def test_add_expense_empty_description(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(10, "", "food")

    def test_add_expense_empty_category(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(10, "Lunch", "")

    def test_add_expense_whitespace_description(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(10, "   ", "food")

    def test_add_expense_whitespace_category(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(10, "Lunch", "  ")

    def test_add_expense_non_string_description(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(10, None, "food")

    def test_add_expense_non_string_category(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(10, "Lunch", 42)

    def test_add_expense_category_normalized(self):
        expense = self.manager.add_expense(10, "Lunch", " Food ")
        self.assertEqual(expense["category"], "food")
        self.assertEqual(expense["description"], "Lunch")

    def test_add_expense_description_too_long(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(10, "x" * 501, "food")

    def test_list_empty(self):
        self.assertEqual(self.manager.list_expenses(), [])

    def test_total_empty(self):
        self.assertEqual(self.manager.total(), 0)

    def test_delete_empty_list(self):
        with self.assertRaises(ValueError):
            self.manager.delete_expense("some-id")

    def test_delete_invalid_id(self):
        with self.assertRaises(ValueError):
            self.manager.delete_expense(None)


class TestAppDeleteInvalidNumber(unittest.TestCase):
    def test_delete_invalid_number(self):
        import subprocess
        result = subprocess.run(
            ["python", "-m", "app", "delete", "99"],
            capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertIn("Invalid expense number", result.stdout or result.stderr)

    def test_delete_non_numeric_number(self):
        import subprocess
        result = subprocess.run(
            ["python", "-m", "app", "delete", "abc"],
            capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertIn("invalid int value", (result.stdout or "") + (result.stderr or ""))


if __name__ == "__main__":
    unittest.main()
