import sys
import pickle

with open('dictionary.pkl', 'rb') as file:
    dictionary = pickle.load(file)

print(dictionary)