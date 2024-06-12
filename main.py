import tkinter as tk
from tkinter import ttk
from views.budget_view import BudgetView
from views.add_expense_view import AddExpenseView
from views.expense_list_view import ExpenseListView
from views.summary_view import SummaryView
from controllers.budget_controller import BudgetController
from controllers.expense_controller import ExpenseController


def main():
    root = tk.Tk()
    root.title("Advanced Budget Manager")

    budget_controller = BudgetController()
    expense_controller = ExpenseController()

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    budget_view = BudgetView(notebook, budget_controller, expense_controller)
    add_expense_view = AddExpenseView(notebook, expense_controller, budget_view)
    expense_list_view = ExpenseListView(notebook, expense_controller)
    summary_view = SummaryView(notebook, budget_controller, expense_controller)

    notebook.add(budget_view, text="Budget")
    notebook.add(add_expense_view, text="Add expense")
    notebook.add(expense_list_view, text="List of expenses")
    notebook.add(summary_view, text="Monthly summary")

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()


def on_closing(root):
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


if __name__ == "__main__":
    main()
