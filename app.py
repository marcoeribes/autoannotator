import sys
from operator import itemgetter
import itertools

import nltk
nltk.download('wordnet')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import gensim
from gensim.parsing.preprocessing import remove_stopwords

from datetime import datetime

from sheetsAPI import *

import pickle



# camelCasing used for mutable methods, variables & objects
# underscore used for immutable variables & objects

# This method parses the list of ontologies and puts them in a dictionary and list
# Ontology Data Structure:
# {Ontology: [[list_of_Tokenized_Ontology], [List_of_lemmitized_words]]}
def parseOntologies(ontologyClasses):
    terms = open(ontologyClasses)
    ontologies = {}
    for line in terms:
        line = line.strip()
        lineLC = line.lower()
        tokenizedLine = word_tokenize(lineLC)
        ontologies[line] = tokenizedLine

    return ontologies

# Checks file type
def checkFileType(str1):
    sub = str1[len(str1) - 4: len(str1)]
    return sub

# initialize the google sheets drive format regardless of data 
def initialize():
    list1 = []
    row1 = ['Epilepsy', 'Concept', 'Text', 'Span Start', 'Span End', 'Annotated Date', 'Status', 'Type', 'Rule Followed']
    row2 = ['']
    list1.append(row1)
    list1.append(row2)
    return list1

# This method gets list of tokens in text
def tokenize(str1, list1):
    strlc = str1.lower()
    tokenList = []

    for term in list1:
        t = term.lower()
        
        if t in strlc:
            row = []
            i = strlc.index(t)
            j = i + len(t)
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            row = ['#', term, t, i, j, dt, "Needs Review", "Isolated Term", "Token Match"]
            #print(lowerTerm + " " + str(i) + " " + str(j))
            tokenList.append(row)     

    return tokenList

# This method gets list of stemmed or lemmatized strings in text
def lemmitize(str1, dict1, list1, list2):
    wnl = WordNetLemmatizer()
    strlc = str1.lower()
    lemmaList = []

    dictValues = list(dict1.values())
    dictKeys = list(dict1)
    dictLen = len(dict1)

    tokenList = word_tokenize(strlc)
    #remove_sw = [word for word in tokenList if not word in list1]

    for token in tokenList:  # remove_sw
        lemma = wnl.lemmatize(token)
        for i in range(dictLen):
            rowLen = len(dictValues[i])
            newToken = ''
            for j in range(rowLen):
                # check if lemma = token in dictionary, if lemma is not a stop word, and if token is not already in the dictonary values
                if lemma == dictValues[i][j] and lemma not in list1 and token not in dictValues[i]:
                    # append token to list of values in Ontology Dictionary
                    dict1[dictKeys[i]].append(token.lower())
    
    dictValues = list(dict1.values())
    
    for x in range(dictLen): 
        rowLen = len(dictValues[x])
        for y in range(rowLen):
            term = dictValues[x][y]
            if term in str1 and term not in list1:
                i = strlc.index(dictValues[x][y])
                j = i + len(term)
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                # Add Later
                for item in list2:
                    key = dictKeys[x]
                    start = int(float(item[3])) # float needed for ValueError
                    end = int(float(item[4]))

                    if start >= i and j >= end: # if i or j out of range
                        row = ['#', key, term, i, j, dt, "Needs Review", "Encapsulated Term", "Semantic Match to Concept"]
                        lemmaList.append(row)     
                    else:
                        row = ['#', key, term, i, j, dt, "Needs Review", "Encapsulated Term", "Semantic Match to Concept"]
                        lemmaList.append(row)        
    
    lemmaList = list(lemmaList for lemmaList,_ in itertools.groupby(lemmaList))       
    return lemmaList


def semanticAnalysis(str1, dict1, list1, list2):
    wnl = WordNetLemmatizer()
    strlc = str1.lower()
    sentList = []

    dictValues = list(dict1.values())
    dictKeys = list(dict1)
    dictLen = len(dict1)

    sentList = sent_tokenize(strlc)
    # remove_sw = [word for word in tokenList if not word in list1]
    #for sent in sentList:
    #    tokenList = word_tokenize(sent)
    #    for token in tokenList:
    #        if token is in dictKeys and not in list1:

# Updates values from dict1 to dict2
def mergeDict(dict1, dict2):
    for key, value in dict1.items():
        if key in dict2.keys():
            dict2[key] += value
        else:
            dict2[key] = value
    return dict2

def removeDuplicates(dict1):
    for key, value in dict1.items():        
        set1 = set(value)
        newValue = list(set1)
        dict1[key] = newValue
    return dict1

# main
def main(args):
    # Initialize Data
    document = open(args[1])
    documentAsString = document.read()
    wks = currentWorksheet(str(args[1]))
    fileType = ''
    if checkFileType(args[2]) == '.txt':
        fileType = '.txt'
        ontologyDict = parseOntologies(args[2])
    elif checkFileType(args[2]) == '.pkl':
        fileType = '.pkl'
        with open('dictionary.pkl', 'rb') as file:
            ontologyDict = pickle.load(file)
    else:
        print("Incorrect File Type")
        quit()
    stopWords = set(stopwords.words('english'))
    for i in range(10):
        stopWords.add(str(i))

    # Initialize drive format
    defaultList = initialize()

    # Tokenize
    tokenList = tokenize(documentAsString, ontologyDict)
    tokenListLen = len(tokenList)
    
    # Lemmatize and Semantically Analyze
    lemmaList = lemmitize(documentAsString, ontologyDict, stopWords, tokenList)
    lemmaListLen = len(lemmaList)
    
    # Sentence Division
    # sentence semanticAnalysis(documentAsString, ontologyDict, stopWords, tokenList)

    # Combine lists
    completeList = defaultList + tokenList + lemmaList
    listLen = len(completeList) + 4
    print(lemmaListLen)

    # Remove duplicates
    #completeList = set(tuple(x) for x in completeList)
    #completeList = [ list(x) for x in completeList ]

    # sort list
    #completeList = sorted(completeList, key=itemgetter(3))
    
    # Add to google sheets
    sheetsCells = 'A1:J' + str(listLen)
    wks.update(sheetsCells, completeList)
    
    # Update Saved Ontology Dictionary
    with open('dictionary.pkl', 'rb') as file:
        oldDict = pickle.load(file)
    newDict = mergeDict(ontologyDict, oldDict)
    newDict = removeDuplicates(newDict)
    with open('dictionary.pkl', 'wb') as file:
        pickle.dump(newDict, file)

# Defaults to pythons main function
if __name__ == '__main__':
    main(sys.argv)

print("\nGoogle Drive Updated Successfully")
quit()