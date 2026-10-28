import math
import uuid
from datetime import datetime

from storage import Storage


class ExpenseManager:
    def __init__(self, filepath="expenses.json"):
        self.storage = Storage(filepath)

    def add_expense(self, amount, description, category="general"):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise ValueError("Amount must be a positive number.")
        if not math.isfinite(amount) or amount <= 0:
            raise ValueError("Amount must be a positive number.")
        if not isinstance(description, str):
            raise ValueError("Description must be a non-empty string.")
        if not description.strip():
            raise ValueError("Description must not be empty or whitespace.")
        description = description.strip()
        if len(description) > 500:
            raise ValueError("Description must be 500 characters or fewer.")
        if not isinstance(category, str):
            raise ValueError("Category must be a non-empty string.")
        if not category.strip():
            raise ValueError("Category must not be empty or whitespace.")
        category = category.strip().lower()
        expense = {
            "id": str(uuid.uuid4()),
            "amount": round(amount, 2),
            "description": description,
            "category": category,
            "date": datetime.now().isoformat(),
        }
        expenses = self.storage.load()
        expenses.append(expense)
        self.storage.save(expenses)
        return expense

    def list_expenses(self, category=None):
        expenses = self.storage.load()
        if category:
            category = category.strip().lower()
            expenses = [e for e in expenses if e["category"] == category]
        return expenses

    def total(self, category=None):
        expenses = self.list_expenses(category)
        return round(sum(e["amount"] for e in expenses), 2)

    def delete_expense(self, expense_id):
        if not isinstance(expense_id, str) or not expense_id.strip():
            raise ValueError("Invalid expense ID.")
        expenses = self.storage.load()
        original_count = len(expenses)
        expenses = [e for e in expenses if e["id"] != expense_id]
        if len(expenses) == original_count:
            raise ValueError("Expense not found.")
        self.storage.save(expenses)
        return True
