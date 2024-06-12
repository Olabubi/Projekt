import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from database import Database


class AddExpenseView(ttk.Frame):
    def __init__(self, parent, controller, budget_view):
        super().__init__(parent)
        self.controller = controller
        self.budget_view = budget_view

        ttk.Label(self, text="Data:").grid(row=0, column=0, sticky=tk.W)
        self.date_entry = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self, text="Opis:").grid(row=1, column=0, sticky=tk.W)
        self.description_entry = ttk.Entry(self)
        self.description_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self, text="Kategoria:").grid(row=2, column=0, sticky=tk.W)
        self.category_entry = ttk.Combobox(self, values=Database.CATEGORIES)
        self.category_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self, text="Kwota:").grid(row=3, column=0, sticky=tk.W)
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

        self.add_button = ttk.Button(self, text="Dodaj", command=self.add_expense)
        self.add_button.grid(row=4, column=0, columnspan=2)

    def add_expense(self):
        date = self.date_entry.get_date()
        description = self.description_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()

        if not date or not description or not category or not amount:
            messagebox.showwarning("Błąd", "Wszystkie pola są wymagane!")
            return

        try:
            amount = float(amount)
            self.controller.add_expense(date, description, category, amount)
            self.budget_view.update_budget_display()
            if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz dodać ten wydatek?"):
                self.controller.add_expense(date, description, category, amount, self.budget_view)
                messagebox.showinfo("Sukces", "Wydatek dodany pomyślnie!")
                self.budget_view.update_budget_display()
        except ValueError:
            messagebox.showwarning("Błąd", "Nieprawidłowa kwota")
