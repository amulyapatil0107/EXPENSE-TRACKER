import os
import tempfile
from src.expense_tracker.tracker import ExpenseTracker
from src.expense_tracker.expense import Expense

def test_add_and_total():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "expenses.json")
        tracker = ExpenseTracker(data_file=data_file)
        assert tracker.get_total() == 0

        tracker.add_expense(Expense(10.0, "food", "lunch", "2026-03-25"))
        tracker.add_expense(Expense(5.0, "transport", "bus", "2026-03-25"))

        assert len(tracker.get_expenses()) == 2
        assert tracker.get_total() == 15.0
        assert tracker.get_total_by_category("food") == 10.0


def test_filter_by_category():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "expenses.json")
        tracker = ExpenseTracker(data_file=data_file)
        tracker.add_expense(Expense(10.0, "food", "dinner", "2026-03-25"))
        tracker.add_expense(Expense(1.0, "food", "water", "2026-03-25"))
        tracker.add_expense(Expense(20.0, "rent", "monthly", "2026-03-25"))

        foods = tracker.get_expenses_by_category("food")
        assert len(foods) == 2
        assert abs(tracker.get_total_by_category("food") - 11.0) < 1e-9

        summary = tracker.get_summary()
        assert summary["count"] == 3
        assert summary["by_category"]["food"] == 11.0

        # edit
        expense_id = tracker.get_expenses()[0].id
        assert tracker.edit_expense(expense_id, amount=12.0, description="updated")
        assert abs(tracker.get_expense_by_id(expense_id).amount - 12.0) < 1e-9

        # delete
        assert tracker.delete_expense(expense_id)
        assert tracker.get_expense_by_id(expense_id) is None
