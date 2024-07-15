import os  # for handling the console output
import time  # for waiting function


class StarSystem:

    accountList = []
    next_account_id = 1 # next available account ID (for auto generating ID)


    def __init__(self, username=None): # Note: balance is the amount of money in an account.
        self.username = username
        self.balance = 0
        self.account_id = None


    def __del__(self):
        if self.username is not None and self.balance is not None:
            msg = "Account {} is now terminated. You have {} in your balance.".format(self.username, self.balance)
            return msg


    def clear_console(self): # clear console when needed
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For *NIX (Handle Jupyter Notebook environment of UIC)
        else:
            os.system('clear')


    def countdown(self, seconds): # For waiting functionality.
        for i in range(seconds, 0, -1):
            print("Wait for the next operation: {}...\r".format(i), end='\r')
            time.sleep(1)
        self.clear_console()


    def createAccount(self):
        self.clear_console()
        username = input("Welcome to -StarSystem- .Your account's secure and smart manager.\nTo register, enter your account name:\n> ").strip()
        if not username:
            self.clear_console()
            print("You must not use an empty username!")
            return
        else: 
            self.username = username
            self.account_id = StarSystem.next_account_id # Set the account ID for the current object
            StarSystem.next_account_id += 1 # increase account_id by 1 for the next account
            StarSystem.accountList.append(self) # add the current account to the accountList
            self.balance = 0 # default balance is 0 for every new account
            self.clear_console()
            print("{}, Welcome! (ID: {})".format(self.username, self.account_id))
            

    def withdraw(self, amount):
        if self.account_id is None:
            print("You must create an account or login first!")
            return # go back to the if judgement until there's a valid user
        self.clear_console()
        print("Account ID: {} tries to withdraw ${}.".format(self.account_id, amount))
        if self.antiFraud(amount): # this is the "if True" statement.
            if amount <= self.balance:
                self.balance -= amount
                print("Account ID: {} (name:{}) has withdrawn ${}. Now has {}".format(self.account_id, self.username, amount, self.balance))
            else:
                print("Not enough balance!")


    def deposit(self, amount):
        self.clear_console()

        if self.account_id is None:
            print("You must create an account or login first!")
            return 

        if amount <= 0:
            print("Invalid amount! Amount must be greater than zero.")
            return

        print("Account ID: {} tries to deposit ${}.".format(self.account_id, amount))

        if self.antiFraud(amount):
            self.balance += amount
            print("Account ID: {} (name:{}) has deposited ${}. Now has {}".format(self.account_id, self.username, amount, self.balance))


    def transfer(self, name_to, bank_to, amount):
        if self.account_id is None:
            print("You must create an account first!")
            return

        account_to = None
        for account in StarSystem.accountList:
            if account.username == name_to:
                account_to = account

        if not account_to:
            print("Recipient account '{}' not found.".format(name_to))
            self.countdown(3)
            return

        if bank_to.strip() == "":
            print("Bank name must not be empty.")
            self.countdown(3)
            return

        try:
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            elif amount != round(amount, 2):
                raise ValueError("Please enter a positive number with at most 2 decimal places.")
        except ValueError as e:
            print("Invalid amount! {}".format(e))
            return

        self.clear_console()
        print("Account ID: {} (name: {}) tries to transfer ${} to Account ID: {} (name:{}) in the {} bank.".format(self.account_id, self.username, amount, account_to.account_id, name_to, bank_to))
        
        if self.antiFraud(amount):
            if amount <= self.balance:
                self.balance -= amount
                account_to.balance += amount
                print("Account ID: {} (user{}) now has {}. Account ID: {} (user{}) now has {}.".format(self.account_id, self.username, self.balance, account_to.account_id, account_to.username, account_to.balance))
            else:
                print("Not enough balance!")


    def antiFraud(self, amount):
        if amount > 10000:  # If user tries to withdraw / transfer / deposit more than $10000, it is considered as fraud-possible. Ask for confirmation.
            confirmation = input("Detected trying to deal with more than $10000. To confirm, type 'Confirm' (MUST EXACTLY MATCH) and press enter.\n> ")
            if confirmation != "Confirm":
                self.clear_console()
                print("Last action stopped due to high chance of fraud.\n")  # If no confirmation, stop the deal.
                self.countdown(3)
                return False
        print("No fraud risk. Continue as normal.")
        return True


def find_account_by_username(username):
    for account in StarSystem.accountList:
        if account.username == username:
            return account
    return None

# begin main
def clear_console():
    if os.name == 'nt': # initialize console
        os.system('cls')
    else:
        os.system('clear')


current_account = None


while True:
    clear_console()
        
    print("-----STAR SYSTEM-----")
    print("YOUR BEST BANK MANAGER\n")
    if current_account is not None:
        print("Current account: {} (ID: {})\n".format(current_account.username, current_account.account_id))
    else:
        print("No account currently logged in.\n")

    print("Choose an option:")
    print("0: Create Account")
    print("1: Login")
    print("2: Deposit")
    print("3: Withdraw")
    print("4: Transfer")
    print("5: Check Balance")
    print("D: Delete Account")
    print("X: Exit")


    choice = input("> ")


    if choice == "0":
        clear_console()
        new_account = StarSystem()
        new_account.createAccount()
        current_account = new_account
        
    elif choice == "1":
        clear_console()
        username = input("Enter the username of the account you want to login:\n> ")
        account = find_account_by_username(username)
        if account is not None:
            current_account = account
            clear_console()
            print("Logged in as: {}".format(username))
        else:
            print("Account not found.")

    elif choice == "2":
        clear_console()
        if current_account is not None:
            try:
                amount = float(input("Enter amount to deposit:\n> "))
                if amount != round(amount, 2):
                    raise ValueError
                current_account.deposit(amount)
            except ValueError as e:
                clear_console()
                print("Invalid amount! Please enter a positive number with at most 2 decimal places.")
        else:
            print("No account logged in. Please log in first.")

    elif choice == "3":
        clear_console()
        if current_account is not None:
            try:
                amount = float(input("Enter amount to withdraw:\n> "))
                if amount <= 0:
                    raise ValueError("Amount must be greater than zero.")
                elif amount != round(amount, 2):
                    raise ValueError("Please enter a positive number with at most 2 decimal places.")
                current_account.withdraw(amount)
            except ValueError as e:
                clear_console()
                print("Invalid amount! {}".format(e))
        else:
            print("No account logged in. Please log in first.")

    elif choice == "4":
        clear_console()

        if current_account is not None:
            while True:
                try:
                    name_to = input("What's the user's name you want to transfer money to?\n> ")
                    if name_to.strip() == "":
                        raise ValueError("Target user must not be empty.")
                    break
                except ValueError as e:
                    print("Invalid target user! {}".format(e))
            while True:
                try:
                    amount = float(input("How much money you want to transfer?\n> "))
                    if str(amount).strip() == "":
                        raise ValueError("Amount must not be empty.")
                    elif amount <= 0:
                        raise ValueError("Amount must be greater than zero.")
                    elif amount != round(amount, 2):
                        raise ValueError("Please enter a positive number with at most 2 decimal places.")
                    break
                except ValueError as e:
                    print("Invalid amount! {}".format(e))
                    continue

            while True:
                try:
                    bank_to = input("Which bank does the target account belong to?\n> ")
                    if bank_to == "":
                        raise ValueError("Must specify a target bank.")
                    break
                except ValueError as e:
                    print("Invalid amount! {}".format(e))
                    continue
            current_account.transfer(name_to, bank_to, amount)

        else:
            print("No account logged in. Please log in first.")
            
    elif choice == "5":
        clear_console()
        if current_account is not None:
            print("Current balance: {}".format(current_account.balance))
        else:
            print("No account logged in. Please log in first.")

    elif choice == "D":
        clear_console()
        if current_account is not None:
            StarSystem.accountList.remove(current_account)
            del current_account
            current_account = None
            print("Account deleted.")
        else:
            print("No account logged in. Please log in first.")

    elif choice == "X":
        clear_console()
        break

    else:
        print("Invalid choice. Please choose again.")


    input("Press Enter to continue...")


    clear_console() # clear again at last to prevent unwanted garbage on screen.
