# Knowtator - EpiKnowtator

## File Overview

 	CLASSICS
	Directory consisting of all research documents in .txt format

	app.py
	Main Python Program that performs name entity recognition on documents and uploads them to Google sheets drive

	service_account.json
	Service account that contains all Google Drive credentials

	sheetsAPI.py
	Python Program that connects to Google Drive

	dictionary.pkl
	A python dictionary that is consistently updated and used to reference different ontologies and their values

	OntologyClasses.txt
	list of all ontologies, used when dicionary.pkl is empty.

	'open dictionary.py'
	Python Progrram that opens contents of the 'dictionary.pkl' file in console

	'update dictioanry.py'
	Python Program that lets user update the 'dictionary.pkl' key-value pairs

## Installation

### Dependencies

    python version 3.8
    nltk version 3.6.5
    gensim version 4.1.2

Ensure you are running python 3.8 and have downloaded the following packages:
		* Refer to requirements.txt file

Ensure that the file(s) you want to process are in the same directory as app.py, including the ontology class!

After downloading all the prerequsites, run the app.py in console:
		python app.py 'document.txt' 'ontologyClasses.txt'
		OR
		'python app.py 'document.txt' 'dictionary.pkl'


## How to Run

1) Open the terminal.
2) In the terminal, locate the path of the folder that contains the file "app.py".
* Hint: Should be in the same folder as this README file
3) Type the command "python app.py 'file name' 'ontologyClasses.txt'" or "python app.py 'file name' 'dictionary.pkl'"
* Example: "python app.py '1998 Luders Semiologic Seizure Classification Corpus.txt' 'dictionary.pkl'

## Format of input files
There are two types of input files the program reads from: labels file and directory of samples.
1. Labels file: the file is of the following format:
	* file_type/sample_num label_list
	* So for instance, if the sample is number 4456 in your directory, it is part of the training set, and the 
		sample labels are ["sports", "politics"], then the line in the labels file should be:
		
					training/4456 sports politics

2. Directory of samples: this is a directory of .txt files, whose names are all numbers. This distinction is important
				because the program parsing converts the name of the .txt file to an integer, that is 
				used as a key in a dictionary


## Useful Research

SciKit Learn - A machine learning library in Python that supports a variety of machine learning algorithms such as clustering, random forests, neural networks, boosting, gradient boosting, k-means, and more. This package could potentially be used to annotate similar words in the text.

NumPy and pandas- SciKit Learn is most often used alongside with NumPy and pandas as NumPy allows for a large collection of data stored as arrays or matrices and pandas has a lot of built in functions that can manipulate the data. This data will then be passed to library functions in SciKit Learn to learn from.

Word2Vec - This library specifically utilizes neural networks to find words that are related to other words in context. To start, the input is a large text and the output will be a large matrix with each word having its own vector. These vector spaces are positioned in such a way that the distance is close to one another if words share common context. Implementing this library can be done with a variety of different Python libraries such as NLTK, Gensim, or tensorflow. 

NLTK - Natural Language Toolkit is a library in Python that supports natural language processing (NLP). This library has a myriad of functions that will analyze the linguistic structure of the text and tokenize the text to further support stemming of the tokens. We primarily used this library to support stemming thus far since it was easy to use and produced great results. Specifically, we can use the PorterStemmer() function, as well as word_tokenize(). 

## Bayes Algo Summary and How to find the probability

In machine learning we are often interested in selecting the best hypothesis (h) given data (d).

In a classification problem, our hypothesis (h) may be the class to assign for a new data instance (d).

One of the easiest ways of selecting the most probable hypothesis given the data that we have that we can use as our prior knowledge about the problem. Bayes’ Theorem provides a way that we can calculate the probability of a hypothesis given our prior knowledge.

Bayes’ Theorem is stated as:

P(h|d) = (P(d|h) * P(h)) / P(d)

Where

P(h|d) is the probability of hypothesis h given the data d. This is called the posterior probability.
P(d|h) is the probability of data d given that the hypothesis h was true.
P(h) is the probability of hypothesis h being true (regardless of the data). This is called the prior probability of h.
P(d) is the probability of the data (regardless of the hypothesis).
You can see that we are interested in calculating the posterior probability of P(h|d) from the prior probability p(h) with P(D) and P(d|h).

After calculating the posterior probability for a number of different hypotheses, you can select the hypothesis with the highest probability. This is the maximum probable hypothesis and may formally be called the maximum a posteriori (MAP) hypothesis.

This can be written as:

MAP(h) = max(P(h|d))

or

MAP(h) = max((P(d|h) * P(h)) / P(d))

or

MAP(h) = max(P(d|h) * P(h))

The P(d) is a normalizing term which allows us to calculate the probability. We can drop it when we are interested in the most probable hypothesis as it is constant and only used to normalize.

Back to classification, if we have an even number of instances in each class in our training data, then the probability of each class (e.g. P(h)) will be equal. Again, this would be a constant term in our equation and we could drop it so that we end up with:

MAP(h) = max(P(d|h))

## Future plans
Currently, the program just tokenizes the words and computes conditional probabilities from there. A better metric that we weren't able 
to implement was the TF-IDF protocol for text vectorization. Some helpful links are below:
	https://en.wikipedia.org/wiki/Tf%E2%80%93idf
	https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089
	https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/
	https://www.kaggle.com/selener/multi-class-text-classification-tfidf
	