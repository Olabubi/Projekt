import tkinter as tk
from tkinter import ttk, messagebox

class BudgetView(ttk.Frame):
    def __init__(self, parent, budget_controller, expense_controller):
        super().__init__(parent)
        self.budget_controller = budget_controller
        self.expense_controller = expense_controller

        ttk.Label(self, text="Wybierz miesiąc:").grid(row=0, column=0, sticky=tk.W)
        self.month_combo = ttk.Combobox(self, values=[
            "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06",
            "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12"
        ])
        self.month_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self, text="Budżet:").grid(row=1, column=0, sticky=tk.W)
        self.budget_entry = ttk.Entry(self)
        self.budget_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        self.save_button = ttk.Button(self, text="Zapisz", command=self.save_budget)
        self.save_button.grid(row=2, column=0, columnspan=2)

        self.update_month_combo()

    def save_budget(self):
        try:
            month = self.month_combo.get()
            amount = float(self.budget_entry.get())
            self.budget_controller.set_budget(month, amount)
            self.update_budget_display()
            if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz ustawić ten budżet?"):
                self.budget_controller.set_budget(month, amount)
                messagebox.showinfo("Sukces", "Budżet został pomyślnie ustawiony!")
                self.update_budget_display()  # Aktualizacja wyświetlanego budżetu po jego zapisaniu
        except ValueError:
            messagebox.showwarning("Błąd", "Nieprawidłowa kwota budżetu")

    def update_month_combo(self):
        self.month_combo.set("")

    def update_budget_display(self):
        budget_month = self.month_combo.get()
        if budget_month:
            budget_amount = self.budget_controller.get_budget(budget_month)
            if budget_amount:
                self.budget_entry.delete(0, tk.END)
                self.budget_entry.insert(0, budget_amount)
            else:
                self.budget_entry.delete(0, tk.END)
                self.budget_entry.insert(0, "Brak ustalonego budżetu")
        else:
            self.budget_entry.delete(0, tk.END)
            self.budget_entry.insert(0, "Brak ustalonego budżetu")
