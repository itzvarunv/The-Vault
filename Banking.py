import Verification as f
import random 

def add(balance,users,name):
    while True:
        try:
            add = int(input("Deposit value: "))
            if add <= 0:
                print("Please enter a valid transaction amount!")
            else:
                balance+=add
                break
        except ValueError:
            print("Please try again with integers!")
    group = users[name]
    group[1] = balance
    users[name] = group
    print(f"Successfully added! Current balance is {balance}")
    return users  

def sub(balance,users,name):
    while True:
        try:
            withdraw = float(input("Withdraw value: "))
            if withdraw < 0:
                print("Please enter a valid transaction amount!")
            else:
                if balance < withdraw:
                    print("Insufficient funds!")
                else:
                    balance -= withdraw
                    group = users[name]
                    group[1] = balance
                    users[name] = group
                    print(f"Successfully registered! Current balance is {balance}")
                    break
        except ValueError:
            print("Please try again with integers!")
    return users 

def bal(users,name):
    group = users[name]
    balance = group[1]
    return balance

def CashTransfer(users, name, verified):
    if verified == True:
        balance = bal(users,name)
        receiver = input("The username of receiver: ")
        if receiver in users:
            while True:
                try:
                    trans= int(input("How much to transfer? "))
                    break
                except ValueError:
                    print("Please enter valid integer choices! ")
            if trans <= balance and trans>0:
                verify = f.verify(name,users)
                if verify == True:
                    balance -= trans
                    group = users[name]
                    group[1] = balance
                    users[name] = group
                    group2 = users[receiver]
                    balance2 = bal(users,receiver)
                    balance2 += trans
                    group2 = users[receiver]
                    group2[1] = balance2
                    message = group2[3]
                    message.append(f"You received {trans} from {name}! The current balance is {balance2}.")
                    group2[3] = message
                    users[receiver] = group2
                    print("Transaction successful!")
                else:
                    print("Wrong password transaction cancelled. ")
            else:
                print("Invalid transfer")
        else:
            print("Receiver does not exist")
    else:
        print("Access Denied try again!")
    return users

def Hedge(name,users):
    print("Grow your money by investment in stock market by our trained professionals!")
    print("Your cash in hedge fund will change each time when you Log in!")
    balance = bal(users,name)
    while True:
        try:
            add = int(input("Deposit value: "))
            if add <= 0:
                print("Please enter a valid transaction amount!")
            else:
                if add>balance:
                    print("You have insufficient funds to deposit!")
                else:
                    balance -= add
                    group = users[name]
                    group[1] = balance
                    group = users[name]
                    details = group[2]
                    fund = details[4]
                    fund += add
                    details[4] = fund
                    group[2] = details
                    users[name] = group
                    print("Fund successful!")
                    break
        except ValueError:
            print("Please try again with integers!")
    return users

def fund(name,users):
    group = users[name]
    details = group[2]
    fund = details[4]
    return fund

def grow(name, users):
    group = users[name]
    details = group[2]
    fund = details[4]
    if fund >0:
        roll = random.randint(1, 100)
        if roll <= 60: # Common Hike: 7% to 27%
            hike = random.randint(7, 27)
            fund += fund*(hike/100)
        elif roll <= 75: # Normal Dip: -1% to -30%
            dip = random.randint(1, 30)
            fund -= fund*(dip/100)
            if fund < 0:
                fund = 0
            else:
                pass
        elif roll <= 85: # Moderate Hike: 27% to 47%
            hike = random.randint(27, 47)
            fund+= fund*(hike/100)
        elif roll <= 90: # Major Dip: -30% to -50%
            dip = random.randint(30, 50)
            fund-= fund*(dip/100)
            if fund < 0:
                fund = 0
            else:
                pass
        elif roll <= 95: # Big Hike: 47% to 70%
            hike = random.randint(47, 70)
            fund+= fund*(hike/100)
        else: # Ultra Hike: 70% to 100%
            hike = random.randint(70, 100)
            fund += fund*(hike/100)
        details[4] = fund
        group[2] = details
        users[name] = group
    else:
        pass
    return users

def loan(name,users):
    group = users[name]
    details = group[2]
    cibil = details[2]
    loan = details[3]
    if loan > 0 or cibil < 0:
        print("You are ineligible to apply loan due to an existing loan or you had previously defaulted a loan! ")
    else:
        print("You are eligible to get a loan but remember the following: ")
        print("-You can only get maximum loan of 30% of your balance.")
        print("-The loan has 10% interest and will be deducted for each Log in. ")
        print("-if you defaulted bringing down your cibil score beyond a threshold you will be deinied to take further loans! ")
        ch = input("Do you agree with the terms? (yes/no): ")
        if ch == 'yes':
            while True:
                try:
                    loan = int(input("How much would you like to borrow? "))
                    if loan<0:
                        print("Please enter a valid transaction!")
                    else:
                        balance = bal(users,name)
                        valid = balance*(30/100)
                        if loan > valid:
                            print("You can't take loans greater than 30% of your balance!")
                        else:
                            balance+=loan
                            group = users[name]
                            group[1] = balance
                            details = group[2]
                            details[3] = loan + loan*(10/100)
                            group[2] = details
                            users[name] = group
                            print("Transaction successful!")
                            break
                except ValueError:
                    print("Please enter in integers only!")
                        
        else:
            print("Exiting...")
    return users
        
def deduct(name, users):
    group = users[name]
    details = group[2]
    cibil = details[2]
    loan = details[3]
    if loan > 0:
        balance = bal(users,name)
        pay = loan*(10/100)
        if loan <= 1 and balance>=1:
            balance -= loan
            loan = 0
            cibil = details[2]
            cibil+=10
            group[2] = details
            group[1] = balance
            users[name] = group
            details[2] = cibil
        elif balance >= pay:
            balance -= pay
            group = users[name]
            group[1] = balance
            details = group[2]
            loan-=pay
            details[3] = loan - pay
            group[2] = details
            users[name] = group
        else:
            group = users[name]
            details = group[2]
            cibil = details[2]
            cibil-=10
            details[2] = cibil
            group[2] = details
            users[name] = group
    else:
        pass
    return users
            
            
def PayBack(name,users,verified):
    if verified == True:
        group = users[name]
        details = group[2]
        loan = details[3]
        if loan == 0:
            print("You have no pending loans!")
        else:
            print(f"You have ${loan} pending in loan payments!")
            balance = bal(users,name)
            while True:
                try:
                    pay = float(input("Repay amount: "))
                    if pay<0 or pay>loan or pay > balance:
                        if pay<0:
                            print("Please enter a valid transaction!")
                        elif pay>loan:
                            print("You can't pay more than what you had taken as loan!")
                        else:
                            print("Insufficient funds!")
                    else:
                        loan-=pay
                        if loan == 0:
                            cibil = details[2]
                            cibil+=10
                            details[2] = cibil
                        else:
                            pass
                        balance-=pay
                        group[1] = balance
                        details[3] = loan
                        group[2] = details
                        users[name] = group
                        print("Transaction is done successfully!")
                        break
                except ValueError:
                    print("Please enter valid numbers!")
    else:
        print("Access Denied try again!")
    return users
                            
def GetFund(users,name,verified):
    if verified == True:
        group = users[name]
        details = group[2]
        fund = details[4]
        if fund == 0:
            print("You hadn't invested any cash yet!")
        else:
            print(f"You have ${fund} in investments!")
            balance = bal(users,name)
            while True:
                try:
                    get = float(input("Withdraw amount: "))
                    if get<0 or get> fund:
                        if get<0:
                            print("Please enter a valid transaction!")
                        else:
                            print("You can't withdraw more than what you had deposited!")
                    else:
                        fund-=get
                        balance+=get
                        group[1] = balance
                        details[4] = fund
                        group[2] = details
                        users[name] = group
                        print("Withdrawn successfully!")
                        break
                except ValueError:
                    print("Please enter valid numbers!")
    else:
        print("Access Denied try again!")
    return users

                    
            
    
            
