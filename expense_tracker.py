import csv
import os
from collections import defaultdict

DATA_FILE = os.path.join("data", "expenses.csv")
HEADERS = ["id", "date", "category", "description", "amount"]

class ExpenseTracker:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as file:
                csv.writer(file).writerow(HEADERS)

    def _read(self):
        with open(self.filename, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def _next_id(self):
        rows = self._read()
        ids = [int(row["id"]) for row in rows if row["id"].isdigit()]
        return max(ids, default=0) + 1

    def add_expense(self, date, category, description, amount):
        with open(self.filename, "a", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow([
                self._next_id(), date, category, description, f"{amount:.2f}"
            ])

    def display_expenses(self, category=None):
        rows = self._read()
        if category:
            rows = [r for r in rows if r["category"].lower() == category.lower()]

        if not rows:
            print("\nNo expenses found.")
            return

        print("\n" + "-" * 90)
        print(f"{'ID':<5}{'Date':<14}{'Category':<16}{'Description':<35}{'Amount':>12}")
        print("-" * 90)
        for row in rows:
            print(f"{row['id']:<5}{row['date']:<14}{row['category']:<16}"
                  f"{row['description'][:33]:<35}₹{float(row['amount']):>10.2f}")
        print("-" * 90)

    def total_expense(self):
        return sum(float(row["amount"]) for row in self._read())

    def category_summary(self):
        summary = defaultdict(float)
        for row in self._read():
            summary[row["category"]] += float(row["amount"])
        return dict(summary)

    def display_summary(self):
        summary = self.category_summary()
        if not summary:
            print("\nNo expenses available.")
            return
        print("\nCATEGORY-WISE SUMMARY")
        print("-" * 35)
        for category, amount in sorted(summary.items()):
            print(f"{category:<20} ₹{amount:>10.2f}")
        print("-" * 35)
        print(f"{'TOTAL':<20} ₹{self.total_expense():>10.2f}")

    def delete_expense(self, expense_id):
        rows = self._read()
        remaining = [row for row in rows if int(row["id"]) != expense_id]
        if len(remaining) == len(rows):
            return False

        with open(self.filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(remaining)
        return True
