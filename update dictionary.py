import sys
import pickle

# Make sure that dictionary.pkl is not empty
# If you are unsure, run app.py before 

def main(args):
    with open('dictionary.pkl', 'rb') as file:
        dictionary = pickle.load(file)
    
    key = args[1]
    value = args[2]
    
    if key not in dictionary:
        print("Key \'" + key + "\' not found. Please use a key that is already in the dictionary.")
        quit()
    
    for item in dictionary[key]:
        if value == item:
            print("Value \'" + value + "\' is already in \'" + key + "\' key-value pair")
            quit()
    
    dictionary[key].append(value)

    print("Key-value pair updated: ")
    print(key + ": " + str(dictionary[key]))

    with open('dictionary.pkl', 'wb') as file:
        pickle.dump(dictionary, file)

# Defaults to pythons main function
if __name__ == '__main__':
    main(sys.argv)
    quit()