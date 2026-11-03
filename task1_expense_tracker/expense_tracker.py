import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")


def load_expenses():
    """Loads expense records from a local JSON file on startup."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_expenses(expenses):
    """Persists the in-memory list of expense dictionaries to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    """Prompts the user for amount, category, and date, and saves the entry."""
    print("\n--- Add New Expense ---")
    while True:
        try:
            amount = float(input("Enter expense amount ($): ").strip())
            if amount <= 0:
                print("Error: Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    category = input("Enter category (e.g., Food, Transport, Utilities): ").strip().title() or "General"
    date_input = input("Enter date (YYYY-MM-DD) [Press Enter for today]: ").strip()
    
    if not date_input:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date_str = date_input
        except ValueError:
            date_str = datetime.now().strftime("%Y-%m-%d")

    new_entry = {
        "id": len(expenses) + 1,
        "amount": round(amount, 2),
        "category": category,
        "date": date_str
    }
    expenses.append(new_entry)
    save_expenses(expenses)
    print(f"Added ${new_entry['amount']:.2f} under '{new_entry['category']}' on {new_entry['date']}.")


def view_expenses(expenses):
    """Displays all stored expenses."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print(f"\n{'ID':<4} | {'Date':<12} | {'Category':<15} | {'Amount ($)':>10}")
    print("-" * 48)
    for item in expenses:
        print(f"{item['id']:<4} | {item['date']:<12} | {item['category']:<15} | ${item['amount']:>9.2f}")


def monthly_summary_report(expenses):
    """Bonus: Monthly summary report using f-strings and category aggregation."""
    if not expenses:
        print("\nNo expenses available.")
        return

    month_prefix = input("Enter month (YYYY-MM, e.g., 2026-11): ").strip()
    monthly_records = [e for e in expenses if e["date"].startswith(month_prefix)]

    if not monthly_records:
        print(f"No records found for '{month_prefix}'.")
        return

    category_buckets = {}
    for exp in monthly_records:
        cat = exp["category"]
        category_buckets.setdefault(cat, []).append(exp["amount"])

    overall_total = sum(e["amount"] for e in monthly_records)
    print(f"\n=== Summary for {month_prefix} (Total: ${overall_total:.2f}) ===")
    for cat, amounts in category_buckets.items():
        print(f"- {cat}: Total = ${sum(amounts):.2f} | Average = ${sum(amounts)/len(amounts):.2f}")


def main():
    expenses = load_expenses()
    while True:
        print("\n1. Add Expense | 2. View Expenses | 3. Monthly Summary | 4. Exit")
        choice = input("Select option (1-4): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            monthly_summary_report(expenses)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
