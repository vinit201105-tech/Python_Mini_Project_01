import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILENAME = "expenses.json"

def load_expenses():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_expenses(expenses):
    with open(FILENAME, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense():
    description = input("Enter description: ")
    try:
        amount = float(input("Enter amount (₹): "))
    except ValueError:
        print("Invalid amount!")
        return
    category = input("Enter category (Food/Travel/Bills/Shopping/Other): ").capitalize()
    date = datetime.now().strftime("%Y-%m-%d")
    expenses = load_expenses()
    expenses.append({"date": date, "description": description, "amount": amount, "category": category})
    save_expenses(expenses)
    print("Expense added successfully!")

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet!")
        return
    print("\n====== Expense List ======")
    print(f"{'Date':<12} {'Description':<20} {'Category':<12} {'Amount (₹)':>10}")
    print("-" * 58)
    total = 0
    for e in expenses:
        print(f"{e['date']:<12} {e['description']:<20} {e['category']:<12} {e['amount']:>10.2f}")
        total += e['amount']
    print("-" * 58)
    print(f"{'Total Spent:':<46} ₹{total:.2f}\n")

def show_summary():
    expenses = load_expenses()
    if not expenses:
        print("No data to analyze!")
        return
    category_total = {}
    for e in expenses:
        category_total[e["category"]] = category_total.get(e["category"], 0) + e["amount"]
    print("\n====== Expense Summary ======")
    for cat, amt in category_total.items():
        print(f"{cat:<15}: ₹{amt:.2f}")
    print(f"{'-'*30}\nTotal: ₹{sum(category_total.values()):.2f}\n")
    plt.figure(figsize=(6, 4))
    plt.bar(category_total.keys(), category_total.values())
    plt.title("Expense by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.tight_layout()
    plt.show()
    plt.figure(figsize=(5, 5))
    plt.pie(category_total.values(), labels=category_total.keys(), autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.show()

def monthly_report():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to show!")
        return
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")
    filtered = [e for e in expenses if e["date"].startswith(f"{year}-{month.zfill(2)}")]
    if not filtered:
        print("No records for this month!")
        return
    print(f"\n====== Report for {month}/{year} ======")
    total = 0
    for e in filtered:
        print(f"{e['date']} | {e['description']} | ₹{e['amount']} | {e['category']}")
        total += e['amount']
    print(f"\nTotal spent in {month}/{year}: ₹{total:.2f}")

def main():
    while True:
        print("\n========== EXPENSE TRACKER ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Summary (Charts)")
        print("4. Monthly Report")
        print("5. Exit")
        print("=====================================")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            monthly_report()
        elif choice == "5":
            print("Exiting... Have a great day!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
