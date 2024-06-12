import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class ExpenseListView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Filtruj po kategorii:").pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.category_filters = {}
        for category in Database.CATEGORIES:
            self.category_filters[category] = tk.BooleanVar()

        for category, var in self.category_filters.items():
            ttk.Checkbutton(self, text=category, variable=var, command=self.update_expense_list).pack(side=tk.TOP, anchor=tk.W, padx=5)

        self.refresh_button = ttk.Button(self, text="Odśwież", command=self.update_expense_list)
        self.refresh_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Data", "Opis", "Kategoria", "Kwota"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Opis", text="Opis")
        self.tree.heading("Kategoria", text="Kategoria")
        self.tree.heading("Kwota", text="Kwota")
        self.tree.pack(expand=True, fill='both')

        self.update_expense_list()

        self.delete_button = ttk.Button(self, text="Usuń wydatek", command=self.delete_expense)
        self.delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def delete_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            expense_id = self.tree.item(selected_item, 'values')[0]
            self.controller.delete_expense(expense_id)
            self.update_expense_list()
        else:
            messagebox.showwarning("Błąd", "Wybierz wydatek do usunięcia!")

    def update_expense_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        selected_categories = [category for category, var in self.category_filters.items() if var.get()]

        expenses = self.controller.get_expenses(selected_categories)
        for expense in expenses:
            self.tree.insert("", "end", values=expense)
