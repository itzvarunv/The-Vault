import bcrypt
import Banking as b

def details():
    valid = True
    print("We have to verify few things before signing up!")
    name = input("What's your name? ")
    while True:
        try:
            age = int(input("Age in integers: "))
            break
        except ValueError:
            print("Please try again with integers!")
    if age < 0:
        print("Impossible age detected")
        valid = False
    elif age <18:
        print("We don't provide child account")
        valid = False
    else:
        pass
    details = [name,age,0,0,0] #Name, Age, Cibil Score, Loan, Mutual fund
    return details,valid

def SignUp(details, verified, users):
    while True:
        name = input("Create a username: ")
        if name in users:
            print("Uh oh this username is already in use try with another!")
        else:
            break
    password = input("That's sweet now give the password: ")
    password = password.encode('utf-8') 
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    users[name] = [hashed_password,0,details,[]] #Password, Balance, Account details, messages
    user = name
    verified = True
    return verified, name, users

def transfers(name,users):
    if name in users:
        group = users[name]
        messages = group[3]
        if len(messages) >= 1:
            for message in messages:
                print(message)
            messages = []
            group[3] = messages
            users[name] = group
        else:
            pass
    else:
        pass
    return users

def LogIn(verified, users):
    name = input("What's your username? ")
    if name in users:
        couple = users[name]    #couple = [password, balance, details, messages]
        verify = couple[0]     
        password = input("Enter your password: ")
        password = password.encode('utf-8') 
        if bcrypt.checkpw(password, verify):
            print("Password matched! Access granted.")
            users = transfers(name,users)
            users = b.grow(name, users)
            users = b.deduct(name, users)
            verified = True
        else:
            print("Incorrect password.")
    else:
        print("User does not exist")
    return verified, name, users

def verify(name,users):
    password = input("Enter your password: ")
    password = password.encode('utf-8')
    couple = users[name]    #couple = [password, balance, details, messages]
    verify = couple[0] 
    if bcrypt.checkpw(password, verify):
        print("Password matched! Access granted.")
        verified = True
    else:
        print("Incorrect password.")
        verified = False
    return verified

def ChangePass(name,users,verified):
    if verified:
        password = input("New password: ")
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt) 
        group = users[name]
        group[0] = hashed_password  # Save the hashed password
        print("Changed successfully!")
    else:
        print("Access Denied. Try again!")
    return users


    
        
    
    
