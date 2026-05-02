'''Proving that the password is hashed and cannot be decoded'''
import pickle

'''with open("users.dat", "wb") as f:
    j = {}
    pickle.dump(j,f)'''

with open("users.dat", "rb") as f:
    j = pickle.load(f)

print(j)
