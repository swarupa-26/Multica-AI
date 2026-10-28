# Command-Line Interface (CLI) code
import sys
import argparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from expense_manager import ExpenseManager


def main():
    print("Expense Tracker")
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("amount", type=float, help="Expense amount")
    add_parser.add_argument("description", help="Expense description")
    add_parser.add_argument("--category", default="general", help="Category (default: general)")

    list_parser = subparsers.add_parser("list", help="List expenses")
    list_parser.add_argument("--category", help="Filter by category")

    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("number", type=int, help="Expense number to delete")

    summary_parser = subparsers.add_parser("summary", help="Show spending summary")

    args = parser.parse_args()
    manager = ExpenseManager()

    if args.command == "add":
        try:
            expense = manager.add_expense(args.amount, args.description, args.category)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        print(f"Expense added successfully: ₹{expense['amount']:.2f} - {expense['description']} [{expense['category']}]")

    elif args.command == "list":
        expenses = manager.list_expenses(category=args.category)
        if not expenses:
            print("No expenses found.")
            sys.exit(1)
        for i, e in enumerate(expenses, 1):
            print(f"  {i}. ₹{e['amount']:.2f}  [{e['category']}]  {e['description']}")
        total = manager.total(category=args.category)
        print(f"Total expenses: ₹{total:.2f}")

    elif args.command == "delete":
        expenses = manager.list_expenses()
        if not expenses:
            print("No expenses found.")
            sys.exit(1)
        for i, e in enumerate(expenses, 1):
            print(f"  {i}. ₹{e['amount']:.2f}  {e['description']:<30}  [{e['category']}]")
        try:
            num = int(args.number)
            if num < 1 or num > len(expenses):
                print("Error: Invalid expense number.")
                sys.exit(1)
        except ValueError:
            print("Error: Please provide a valid number.")
            sys.exit(1)
        expense = expenses[num - 1]
        manager.delete_expense(expense["id"])
        print(f"Deleted expense: ₹{expense['amount']:.2f} - {expense['description']}")

    elif args.command == "summary":
        total = manager.total()
        print(f"Total expenses: ₹{total:.2f}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
