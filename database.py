import sqlite3

class Database:
    CATEGORIES = ["Jedzenie", "Transport", "Rachunki", "Rozrywka", "Inne"]

    def __init__(self):
        self.conn = sqlite3.connect("budget_manager.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS budget
                               (id INTEGER PRIMARY KEY, month TEXT, amount REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                               (id INTEGER PRIMARY KEY, date TEXT, description TEXT, category TEXT, amount REAL)''')
        self.conn.commit()

    def add_budget(self, month, amount):
        self.cursor.execute("INSERT INTO budget (month, amount) VALUES (?, ?)", (month, amount))
        self.conn.commit()

    def get_budget(self, month):
        self.cursor.execute("SELECT amount FROM budget WHERE month = ? ORDER BY id DESC LIMIT 1", (month,))
        result = self.cursor.fetchone()
        return result

    def add_expense(self, date, description, category, amount):
        self.cursor.execute("INSERT INTO expenses (date, description, category, amount) VALUES (?, ?, ?, ?)",
                            (date, description, category, amount))
        self.conn.commit()

    def get_expenses(self, month=None, categories=None):
        query = "SELECT id, date, description, category, amount FROM expenses"
        params = []

        if month and categories:
            query += " WHERE strftime('%Y-%m', date) = ? AND category IN ({seq})".format(
                seq=','.join(['?'] * len(categories)))
            params.append(month)
            params.extend(categories)
        elif month:
            query += " WHERE strftime('%Y-%m', date) = ?"
            params.append(month)
        elif categories:
            query += " WHERE category IN ({seq})".format(
                seq=','.join(['?'] * len(categories)))
            params.extend(categories)

        self.cursor.execute(query, params)
        expenses = self.cursor.fetchall()
        return expenses

    def delete_expense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        self.conn.commit()

    def get_monthly_summary(self):
        summary = {}
        cursor = self.conn.cursor()
        cursor.execute("SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM expenses GROUP BY month")
        rows = cursor.fetchall()
        for row in rows:
            month = row[0]
            total_expenses = row[1]
            budget_row = cursor.execute("SELECT amount FROM budget WHERE month = ?", (month,)).fetchone()
            budget = budget_row[0] if budget_row else 0.0
            summary[month] = {"total": total_expenses, "budget": budget, "difference": budget - total_expenses}
        return summary
