import pickle
import Verification as v
import Settings as s
import Banking as b

with open("users.dat","rb") as f:
    users = pickle.load(f)

print("Weclome to The Vault the bank of future.")
print("1. Log In")
print("2. Sign up")

while True:
    try:
        ch = int(input("What do you choose? "))
        break
    except ValueError:
        print("Please enter (1/2) only!")
#Verification
if ch == 1:
    verify = False
    verify, name, users = v.LogIn(verify, users)
    s.save("users.dat",users)

elif ch == 2:
    verify = False
    details,valid = v.details()
    if valid == False:
        print("Can't create an account")
    else:
        verify, name, users = v.SignUp(details, verify, users)
        s.save("users.dat",users)

else:
    print("Invalid choice")
        
while verify == True:
    print("1. Account settings")
    print("2. Banking")
    print("3. About the bank")
    print("4. Exit")
    print()

    while True:
        try:
            ch1 = int(input("Which one do you choose? "))
            break
        except ValueError:
            print("Please enter valid integer choices! ")
    #Settings     
    if ch1 == 1:
        print("1. View account details")
        print("2. Change password")
        print("3. Delete account")
        print("4. Change account details")
        print("Any key for Back")
        print()

        while True:
            try:
                ch2 = int(input("Which one do you choose? "))
                break
            except ValueError:
                print("Please enter valid integer choices! ")

        if ch2 == 1:
            s.account_details(name,users)

        elif ch2 == 2:
            verified = v.verify(name,users)
            users = v.ChangePass(name,users,verified)
            s.save("users.dat",users)

        elif ch2 == 3:
            verified = v.verify(name,users)
            users, verify = s.delete(name,users,verified,verify)
            s.save("users.dat",users)

        elif ch2 == 4:
            verified = v.verify(name,users)
            users = s.ChangeDetails(name, users, verified)
            s.save("users.dat",users)

        else:
            pass
    #Banking   
    elif ch1 == 2:
        print("1. View balance")
        print("2. Withdraw cash")
        print("3. Deposit cash")
        print("4. Transfer cash")
        print("5. Hedge funds")
        print("6. Apply loan")
        print("Any key for Back")
        print()

        while True:
            try:
                ch3 = int(input("Which one do you choose? "))
                break
            except ValueError:
                print("Please enter valid integer choices! ")

        if ch3 == 1:
            balance = b.bal(users,name)
            print(f"Currently you have ${balance}")

        elif ch3 == 2:
            balance = b.bal(users,name)
            verified = v.verify(name,users)
            if verified == True:
                users = b.sub(balance,users,name)
                s.save("users.dat",users)
            else:
                print("Access Denied try again!")

        elif ch3 == 3:
            balance = b.bal(users,name)
            verified = v.verify(name,users)
            if verified == True:
                users = b.add(balance,users,name)
                s.save("users.dat",users)
            else:
                print("Access Denied try again!")

        elif ch3 == 4:
            verified = v.verify(name,users)
            users = b.CashTransfer(users, name, verified)
            s.save("users.dat",users)

        elif ch3 == 5:
            print("1. View funds")
            print("2. Invest")
            print("3. Withdraw funds")
            print("Any key for Back")

            while True:
                try:
                    ch4 = int(input("Which one do you choose? "))
                    break
                except ValueError:
                    print("Please enter valid integer choices! ")

            if ch4 ==1:
                fund = b.fund(name,users)
                print(f"Currently the fund is at ${fund}!")

            elif ch4 == 2:
                verified = v.verify(name,users)
                if verified == True:
                    users = b.Hedge(name,users)
                    s.save("users.dat",users)
                else:
                    print("Access Denied try again!")

            elif ch4 == 3:
                verified = v.verify(name,users)
                users = b.GetFund(users,name,verified)
                s.save("users.dat",users)

            else:
                pass

        elif ch3 == 6:
            print("1. Get loan")
            print("2. Payback existing loan.")
            print("Any key for Back")

            while True:
                try:
                    ch4 = int(input("Which one do you choose? "))
                    break
                except ValueError:
                    print("Please enter valid integer choices! ")

            if ch4 == 1:
                verified = v.verify(name,users)
                if verified == True:
                    users = b.loan(name,users)
                    s.save("users.dat",users)
                else:
                    print("Access Denied try again!")

            elif ch4 == 2:
                verified = v.verify(name,users)
                users = b.PayBack(name,users,verified)
                s.save("users.dat",users)

            else:
                pass

    elif ch1 == 3:
        print("""
=========================================
              WELCOME TO THE VAULT
=========================================

A next-generation banking system engineered with precision,
security, and user control at its core.

Features:
- Encrypted password authentication for secure access
- Instant fund transfers between user accounts
- Ability to change passwords anytime with full control
- Seamless account deletion on user request
- Loan management system with transparent terms
- Hedge fund investment options with peak returns up to 100%
- Intuitive, minimal user interface for a focused experience

Your assets. Your rules. Our technology.

            — The Vault —
        Security. Speed. Sophistication.
=========================================
""")

    elif ch1 == 4:
        print("Good bye :)")
        break
        
