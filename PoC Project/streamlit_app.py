import streamlit as st
from expense_manager import ExpenseManager

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

manager = ExpenseManager()

st.title("💰 Expense Tracker")

# --- Summary ---
st.header("Summary")
total = manager.total()
st.metric("Total Expenses", f"₹{total:.2f}")

# --- Add Expense ---
st.header("Add Expense")
with st.form("add_expense_form", clear_on_submit=True):
    amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
    description = st.text_input("Description")
    category = st.text_input("Category", value="general")
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        try:
            expense = manager.add_expense(amount, description, category)
            st.success(f"Added: ₹{expense['amount']:.2f} - {expense['description']} [{expense['category']}]")
            st.rerun()
        except ValueError as e:
            st.error(str(e))

# --- Expenses ---
st.header("Expenses")
expenses = manager.list_expenses()

if not expenses:
    st.info("No expenses found.")
else:
    for i, e in enumerate(expenses, 1):
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1.5, 0.5])
        col1.write(f"**{i}.**")
        col2.write(f"₹{e['amount']:.2f}")
        col3.write(e['description'])
        col4.write(f"`{e['category']}`")
        if col5.button("🗑️", key=f"delete_{e['id']}"):
            manager.delete_expense(e["id"])
            st.rerun()
