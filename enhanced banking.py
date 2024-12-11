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

class BankAccount:
    def __init__(self, account_number, account_holder, pin, balance=0, transaction_history=None):
        self.account_number = account_number
        self.account_holder = account_holder
        self.pin = pin
        self.balance = balance
        self.transaction_history = transaction_history if transaction_history else []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(
                f"{datetime.datetime.now()} - Deposited ₹{amount}. Balance: ₹{self.balance}"
            )
            print(f"Deposited ₹{amount}. New balance is ₹{self.balance}.")
        else:
            print("Deposit amount must be greater than zero.")

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                self.transaction_history.append(
                    f"{datetime.datetime.now()} - Withdrew ₹{amount}. Balance: ₹{self.balance}"
                )
                print(f"Withdrew ₹{amount}. New balance is ₹{self.balance}.")
            else:
                print("Insufficient balance!")
        else:
            print("Withdrawal amount must be greater than zero.")

    def check_balance(self):
        print(f"Your current balance is ₹{self.balance}.")

    def show_transaction_history(self):
        if self.transaction_history:
            print("\nTransaction History:")
            for transaction in self.transaction_history:
                print(transaction)
        else:
            print("No transactions yet.")

    def to_dict(self):
        return {
            "account_holder": self.account_holder,
            "pin": self.pin,
            "balance": self.balance,
            "transaction_history": self.transaction_history,
        }

# PIN Validation Function
def validate_pin(account):
    for _ in range(3):  # Allow 3 attempts
        entered_pin = input("Enter your PIN: ")
        if entered_pin == account.pin:
            return True
        print("Incorrect PIN. Try again.")
    print("Too many failed attempts. Access denied.")
    return False

# Find an account by account number
def find_account(accounts, account_number):
    if account_number in accounts:
        data = accounts[account_number]
        return BankAccount(
            account_number,
            data["account_holder"],
            data["pin"],
            data["balance"],
            data["transaction_history"],
        )
    else:
        print("Account not found!")
        return None

# Main Program
def main():
    print("Welcome to the Enhanced Banking System")
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
            accounts[account_number] = BankAccount(account_number, account_holder, pin).to_dict()
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
                    amount = float(input("Enter the amount to deposit: "))
                    account.deposit(amount)
                elif acc_choice == '2':
                    amount = float(input("Enter the amount to withdraw: "))
                    account.withdraw(amount)
                elif acc_choice == '3':
                    account.check_balance()
                elif acc_choice == '4':
                    account.show_transaction_history()
                elif acc_choice == '5':
                    accounts[account_number] = account.to_dict()  # Save updated account data
                    save_accounts(accounts)
                    print("Returning to main menu...")
                    break
                else:
                    print("Invalid choice! Please choose again.")

        elif choice == '3':
            print("Thank you for using the Enhanced Banking System. Goodbye!")
            break
        else:
            print("Invalid choice! Please choose again.")

# Run the program
if __name__ == "__main__":
    main()
