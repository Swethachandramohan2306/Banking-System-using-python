import json
import datetime

# File to store account data
DATA_FILE = "accounts.json"

# Load accounts from the file
def load_accounts():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save accounts to the file
def save_accounts(accounts):
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)

# Deposit money to an account
def deposit(account):
    amount = float(input("Enter the amount to deposit: "))
    if amount > 0:
        account["balance"] += amount
        account["transaction_history"].append(f"{datetime.datetime.now()} - Deposited ₹{amount}. Balance: ₹{account['balance']}")
        print(f"Deposited ₹{amount}. New balance is ₹{account['balance']}.")
    else:
        print("Deposit amount must be greater than zero.")

# Withdraw money from an account
def withdraw(account):
    amount = float(input("Enter the amount to withdraw: "))
    if amount > 0:
        if amount <= account["balance"]:
            account["balance"] -= amount
            account["transaction_history"].append(f"{datetime.datetime.now()} - Withdrew ₹{amount}. Balance: ₹{account['balance']}")
            print(f"Withdrew ₹{amount}. New balance is ₹{account['balance']}.")
        else:
            print("Insufficient balance!")
    else:
        print("Withdrawal amount must be greater than zero.")

# Show balance of an account
def check_balance(account):
    print(f"Your current balance is ₹{account['balance']}.")

# Show transaction history
def show_transaction_history(account):
    if account["transaction_history"]:
        print("\nTransaction History:")
        for transaction in account["transaction_history"]:
            print(transaction)
    else:
        print("No transactions yet.")

# Validate PIN for an account
def validate_pin(account):
    for _ in range(3):  # Allow 3 attempts
        entered_pin = input("Enter your PIN: ")
        if entered_pin == account["pin"]:
            return True
        print("Incorrect PIN. Try again.")
    print("Too many failed attempts. Access denied.")
    return False

# Find an account by account number
def find_account(accounts, account_number):
    if account_number in accounts:
        return accounts[account_number]
    else:
        print("Account not found!")
        return None

# Main Program
def main():
    print("Welcome to the Simple Banking System")
    accounts = load_accounts()

    while True:
        print("\nMain Menu:")
        print("1. Create New Account")
        print("2. Access Existing Account")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            account_number = input("Enter a new account number: ")
            if account_number in accounts:
                print("Account number already exists. Try another.")
                continue
            account_holder = input("Enter your name: ")
            pin = input("Set a 4-digit PIN: ")
            accounts[account_number] = {
                "account_holder": account_holder,
                "pin": pin,
                "balance": 0,
                "transaction_history": [],
            }
            save_accounts(accounts)
            print(f"Account created successfully for {account_holder}!")

        elif choice == '2':
            account_number = input("Enter your account number: ")
            account = find_account(accounts, account_number)
            if not account:
                continue

            if not validate_pin(account):
                continue

            while True:
                print("\nAccount Menu:")
                print("1. Deposit Money")
                print("2. Withdraw Money")
                print("3. Check Balance")
                print("4. Show Transaction History")
                print("5. Exit to Main Menu")
                acc_choice = input("Enter your choice (1-5): ")

                if acc_choice == '1':
                    deposit(account)
                elif acc_choice == '2':
                    withdraw(account)
                elif acc_choice == '3':
                    check_balance(account)
                elif acc_choice == '4':
                    show_transaction_history(account)
                elif acc_choice == '5':
                    save_accounts(accounts)
                    print("Returning to main menu...")
                    break
                else:
                    print("Invalid choice! Please choose again.")

        elif choice == '3':
            print("Thank you for using the Simple Banking System. Goodbye!")
            break
        else:
            print("Invalid choice! Please choose again.")

# Run the program
if __name__ == "__main__":
    main()
