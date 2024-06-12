import tkinter as tk
from tkinter import ttk, messagebox

class SummaryView(ttk.Frame):
    def __init__(self, parent, budget_controller, expense_controller):
        super().__init__(parent)
        self.budget_controller = budget_controller
        self.expense_controller = expense_controller

        self.tree = ttk.Treeview(self, columns=("Month", "Budget", "Total Expenses", "Difference"), show="headings")
        self.tree.heading("Month", text="Month")
        self.tree.heading("Budget", text="Budget")
        self.tree.heading("Total Expenses", text="Total Expenses")
        self.tree.heading("Difference", text="Difference")
        self.tree.pack(expand=True, fill='both')

        self.refresh_button = ttk.Button(self, text="Odśwież", command=self.update_summary)
        self.refresh_button.pack(pady=10)

        self.update_summary()

    def update_summary(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        summary = self.expense_controller.get_monthly_summary()
        for month, data in summary.items():
            budget = self.budget_controller.get_budget(month)
            total_expenses = data["total"]
            difference = budget - total_expenses if budget is not None else -total_expenses
            self.tree.insert("", "end", values=(month, budget, total_expenses, difference))

