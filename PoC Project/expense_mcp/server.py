import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP
from expense_manager import ExpenseManager

mcp = FastMCP("Expense Tracker MCP")

manager = ExpenseManager()


@mcp.tool()
def add_expense(amount: float, description: str, category: str = "general") -> dict:
    """Add a new expense."""
    return manager.add_expense(amount, description, category)


@mcp.tool()
def get_expenses(category: str = "") -> list:
    """Get expenses, optionally filtered by category."""
    return manager.list_expenses(category or None)


@mcp.tool()
def get_expense_total(category: str = "") -> float:
    """Get the total expense amount, optionally for a category."""
    return manager.total(category or None)


@mcp.tool()
def delete_expense(expense_id: str) -> bool:
    """Delete an expense using its ID."""
    return manager.delete_expense(expense_id)


if __name__ == "__main__":
    mcp.run()