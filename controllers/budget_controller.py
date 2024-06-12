from database import Database

class BudgetController:
    def __init__(self):
        self.db = Database()

    def set_budget(self, month, amount):
        self.db.add_budget(month, amount)

    def get_budget(self, month):
        budget = self.db.get_budget(month)
        return budget[0] if budget else 0.0
