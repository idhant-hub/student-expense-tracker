"""
Student Expense Tracker
Author: Idhant Mishra
Registration No.: 26MIP10079
"""

from expense_tracker import ExpenseTracker
from datetime import datetime

def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Amount must be greater than 0.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def menu():
    print("\n" + "=" * 55)
    print("          STUDENT EXPENSE TRACKER")
    print("=" * 55)
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Search by Category")
    print("4. Show Total Spending")
    print("5. Category-wise Summary")
    print("6. Delete Expense")
    print("7. Exit")
    print("=" * 55)

def main():
    tracker = ExpenseTracker()
    while True:
        menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            date = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format.")
                continue

            category = input("Category (Food/Travel/Education/Shopping/Other): ").strip().title()
            description = input("Description: ").strip()
            amount = get_float("Amount (₹): ")
            tracker.add_expense(date, category, description, amount)
            print("Expense added successfully!")

        elif choice == "2":
            tracker.display_expenses()

        elif choice == "3":
            category = input("Enter category: ").strip().title()
            tracker.display_expenses(category=category)

        elif choice == "4":
            print(f"\nTotal Spending: ₹{tracker.total_expense():.2f}")

        elif choice == "5":
            tracker.display_summary()

        elif choice == "6":
            tracker.display_expenses()
            try:
                expense_id = int(input("Enter Expense ID to delete: "))
                if tracker.delete_expense(expense_id):
                    print("Expense deleted successfully!")
                else:
                    print("Expense ID not found.")
            except ValueError:
                print("Please enter a valid ID.")

        elif choice == "7":
            print("\nThank you for using Student Expense Tracker!")
            break

        else:
            print("Invalid choice. Please select 1-7.")

if __name__ == "__main__":
    main()
