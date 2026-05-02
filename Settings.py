import pickle

def save(file,users):
    with open(file,"wb") as f:
        pickle.dump(users,f)

def account_details(name,users):
    group = users[name]
    details = group[2]
    print(f"Name: {details[0]}")
    print(f"Age: {details[1]}")
    print(f"Balance: {group[1]}")
    print(f"Cibil Score: {details[2]}")
    print(f"Pending loan payments: {details[3]}")
    print(f"Mutual fund investements: {details[4]}")
    print()


def delete(name,users,verified,verify):
    if verified == True:
        group = users[name]
        details = group[2]
        loan = details[3]
        mutual = details[4]
        bal = group[1]
        if loan == 0 and mutual == 0 and bal == 0:
            users.pop(name)
            print("Account deleted")
            verify = False
        else:
            print("Please withdraw all your cashes,payback all your loans to close your account! \nPlease end your mutual funds!")
    else:
        print("Access Denied try again!")
    return users, verify

def ChangeDetails(name, users, verified):
    group = users[name]
    details = group[2]
    age = details[1]
    if verified == True:
        Name = input("New name: ")
        age+=1
        details[0] = Name
        details[1] = age
        group[2] = details
        users[name] = group
        print("Changed successfully!")
    else:
        print("Access Denied try again!")
    return users


    
