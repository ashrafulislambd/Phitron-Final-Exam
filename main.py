from abc import ABC

uid = 0
def get_uid():
    global uid
    uid += 1
    return str(uid)

class User(ABC):
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Customer(User):
    def __init__(self, name, email):
        super().__init__(name, email)

class Account:
    def __init__(self, user, account_type):
        self.user = user
        self.balance = 0
        if account_type != "savings" and account_type != "cuurent":
            raise Exception("Invalid Account Type.")
        self.account_type = account_type
        self.account_no = get_uid()

    def check_available_balance(self):
        print("Balance: " + str(self.balance))

    def deposit(self, user, amount):
        if user is not self.user:
            raise Exception("You are not allowed to deposit in this account.")
        self.balance += amount
        print("Successfully deposited " + str(amount))

    def withdraw(self, user, amount):
        if user is not self.user:
            raise Exception("You are not allowed to withdraw from this account.")
        if amount > self.balance:
            raise Exception("Withdrawal amount exceeded")
        self.balance -= amount
        print("Successfully withdrawn " + str(amount))

class Admin(User):
    def __init__(self, name, email):
        super().__init__(name, email)

class Transaction:
    def __init__(self, from_account, to_account, amount):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

class Bank:
    def __init__(self, balance):
        self.balance = balance
        self.accounts = []
        self.users = []
        self.transactions = []
        self.loan_records = {}
        self.can_take_loan = True

    def create_user(self, name, email):
        user = User(name, email)
        self.users.append(user)

    def show_transaction_history(self, account=None):
        if account is not None:
            print("Transaction Details of " + account.user.name + ": ")
        else:
            print("Transaction Details of everyone: ")
        for transaction in self.transactions:
            if account is None:
                print("From: " + str(transaction.from_account.user.name) + ", To: " + str(transaction.to_account.user.name) + ", Amount: " + transaction.amount)
            else:
                if transaction.from_account == account:
                    print("Sent " + str(transaction.amount) + " to " + transaction.to_account.user.name)
                elif transaction.to_account == account:
                    print("Received " + str(transaction.amount) + " from " + transaction.from_account.user.name)

    def take_loan(self, account, amount):
        if self.can_take_loan == False:
            raise Exception("Loan isn't available at the moment right now.")
        if amount > self.balance:
            raise Exception("The bank doesn't have enough balance to give loans.")
        if account.account_no in self.loan_records:
            if len(self.loan_records[account.account_no] == 2):
                raise Exception("You can take loan for at most two times.")
            self.loan_records[account.account_no].append(amount)
        else:
            self.loan_records[account.account_no] = [amount]
        
        account.balance += amount
        self.balance -= amount

        print("Successfully loan was provided to " + account.user.name)

    def transfer_money(self, from_account_no, to_account_no, amount):
        if from_account_no == to_account_no:
            raise Exception("Cannot transfer money to own account.")

        from_account = None
        to_account = None
        for account in self.accounts:
            if account.account_no == from_account_no:
                from_account = account
            if account.account_no == to_account_no:
                to_account = account
        if from_account is None or to_account is None:
            raise Exception("Account does not exist.")
        if from_account.balance < amount:
            raise Exception("Not enough fund to make the transfer")
        from_account.balance -= amount
        to_account.balance += amount
        self.transactions.append(Transaction(from_account, to_account, amount))

    def create_account(self, user, admin, type):
        if not isinstance(admin, Admin):
            raise Exception("You don't have authorization to create account.")
        if user not in self.users:
            raise Exception("User is not authorized.")
        account = Account(user, type)
        self.accounts.append(account)
        return account

    def delete_account(self, account, admin):
        if not isinstance(admin, Admin):
            raise Exception("You must be an admin to delete that user")
        self.balance += account.balance
        self.accounts.remove(account)

    def see_all_accounts(self, admin):
        if not isinstance(admin, Admin):
            raise Exception("You must be an admin to see all the users.")
        for account in self.accounts:
            print("User: " + account.user.name + ", Account No: " + account.account_no)

    def total_available_balance(self, admin):
        if not isinstance(admin, Admin):
            raise Exception("You must be an admin")
        balance = self.balance
        for account in self.accounts:
            balance += account.balance
        return balance
    
    def total_loan_amount(self, admin):
        if not isinstance(admin, Admin):
            raise Exception("You must be an admin")
        amount = 0
        for record in self.loan_records:
            amount += sum(self.loan_records[record])
        return amount
    
    def toggle_loan(self, admin):
        if not isinstance(admin, Admin):
            raise Exception("You must be an admin")
        self.can_take_loan = not self.can_take_loan

bank1 = Bank(10000)
admin_user = Admin("Admin User 1", "admin@example.com")

def find_user_by_email(email, bank):
    for user in bank.users:
        if user.email == email:
            return user
    return None

def find_account_by_no(account_no, bank):
    for account in bank.accounts:
        if account.account_no == account_no:
            return account
    return None


def customer_replica():
    while True:
        print("Customer Options")
        print("---------------------")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Check Transaction History")
        print("5. Take Loan")
        print("6. Transfer Amount")
        print("0. Exit to Main Menu")

        inp = int(input("Enter Option: "))
        if inp == 0:
            break
        if inp == 1:
            user_email = input("User Email: ")
            account_no = input("Account No: ")
            amount = int(input("Enter Amount: "))
            account = find_account_by_no(account_no, bank1)
            user = find_user_by_email(user_email, bank1)
            if user is None:
                print("No user exists with this email")
            elif account is None:
                print("Account doesn't exist")
            else:
                try:
                    account.deposit(user, amount)
                    print("Successfully deposited")
                except Exception as error:
                    print(error)
        if inp == 2:
            user_email = input("User Email: ")
            account_no = input("Account No: ")
            amount = int(input("Enter Amount: "))
            user = find_user_by_email(user_email, bank1)
            account = find_account_by_no(account_no, bank1)
            if user is None:
                print("No user exists with this email.")
            elif account is None:
                print("Account doesn't exist.")
            else:
                try:
                    account.withdraw(user, amount)
                    print("Successfully withdrawn")
                except Exception as error:
                    print(error)
        if inp == 3:
            user_email = input("User Email: ")
            account_no = input("Account No: ")
            user = find_user_by_email(user_email, bank1)
            account = find_account_by_no(account_no, bank1)

            if account.user is not user:
                print("The account is not owned by the user.")
            elif user is None:
                print("No user exists with this email.")
            elif account is None:
                print("Account doesn't exist.")
            else:
                try:
                    account.check_available_balance()
                except Exception as error:
                    print(error)
        if inp == 4:
            user_email = input("User Email: ")
            account_no = input("Account No: ")
            user = find_user_by_email(user_email, bank1)
            account = find_account_by_no(account_no, bank1)

            if account.user is not user:
                print("The account is not owned by the user.")
            elif user is None:
                print("No user exists with this email.")
            elif account is None:
                print("Account doesn't exist.")
            else:
                try:
                    bank1.show_transaction_history(account)
                except Exception as error:
                    print(error)
        if inp == 5:
            user_email = input("User Email: ")
            account_no = input("Account No: ")
            amount = int(input("Enter Amount: "))
            account = find_account_by_no(account_no, bank1)
            user = find_user_by_email(user_email, bank1)
            if account.user is not user:
                print("The account is not owned by the user.")
            elif user is None:
                print("No user exists with this email.")
            elif account is None:
                print("Account doesn't exist.")
            else:
                try:
                    bank1.take_loan(account, amount)
                except Exception as error:
                    print(error)

        if inp == 6:
            user_email = input("User Email: ")
            account_no = input("Your account no: ")
            to_account_no = input("Receivee account no: ")
            amount = int(input("Enter Amount: "))
            user = find_user_by_email(user_email, bank1)
            account = find_account_by_no(account_no, bank1)
            receivee = find_account_by_no(to_account_no, bank1)

            if account.user is not user:
                print("The account is not owned by the user.")
            elif user is None:
                print("No user exists with this email.")
            elif account is None:
                print("Account doesn't exist.")
            elif receivee is None:
                print("Invalid Receivee Account No.")
            else:
                try:
                    bank1.transfer_money(account_no, to_account_no, amount)
                except Exception as error:
                    print(error)
        
            

def admin_replica():
    while True:
        print("Admin Options")
        print("------------------")
        print("1. Create User (Customer/Non Admin)")
        print("2. Create Account")
        print("3. Delete Account")
        print("4. See All Accounts")
        print("5. See Total Available Balance")
        print("6. See Total Loan Amount")
        print("7. Toggle Loan Feature On/Off")
        print("0. Exit to Main Menu")

        inp = int(input("Enter Option: "))
        if inp == 0:
            break
        
        if inp == 1:
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            bank1.create_user(name, email)

        if inp == 3:
            account_no = input("Account No: ")
            account = find_account_by_no(account_no, bank1)
            try:
                bank1.delete_account(account, admin_user)
            except Exception as error:
                print(error)

        if inp == 2:
            email = input("Enter Email: ")
            user = find_user_by_email(email, bank1)
            account_type = input("Enter Acount Type (savings/cuurent): ")
            try:
                account = bank1.create_account(user, admin_user, account_type)
                print("Account Created")
                print("Account No: " + account.account_no)
            except Exception as error:
                print(error)

        if inp == 4:
            try:
                bank1.see_all_accounts(admin_user)
            except Exception as error:
                print(error)
        
        if inp == 5:
            try:
                total_balance = bank1.total_available_balance(admin_user)
                print("Total Balance: " + str(total_balance))
            except Exception as error:
                print(error)

        if inp == 6:
            try:
                total_loan = bank1.total_loan_amount(admin_user)
                print("Total Loan Amount: " + str(total_loan))
            except Exception as error:
                print(error)

        if inp == 7:
            try:
                bank1.toggle_loan(admin_user)
                print("Loan Feature On: " + str(bank1.can_take_loan))
            except Exception as error:
                print(error)

def main_replica():
    while True:
        print("Banking System")
        print("--------------------")
        print("1. Customer")
        print("2. Admin")
        print("0. Exit")
        inp = int(input("Enter Option: "))
        if inp == 0:
            break
        if inp == 1:
            customer_replica()
        if inp == 2:
            admin_replica()

main_replica()
        
