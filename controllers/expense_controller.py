from database import Database
from datetime import datetime

class ExpenseController:
    def __init__(self):
        self.db = Database()

    def add_expense(self, date, description, category, amount, budget_view=None):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            amount = float(amount)
        except ValueError:
            raise ValueError("Nieprawidłowy format daty lub kwoty!")

        self.db.add_expense(date, description, category, amount)
        if budget_view:
            budget_month = date[:7]
            budget_amount = self.db.get_budget(budget_month)
            if budget_amount:
                budget_view.update_budget_display()
            else:
                budget_view.update_budget_display(None)

    def get_expenses(self, categories=None, month=None):
        return self.db.get_expenses(categories=categories, month=month)

    def delete_expense(self, expense_id):
        self.db.delete_expense(expense_id)

    def get_monthly_summary(self):
        return self.db.get_monthly_summary()
