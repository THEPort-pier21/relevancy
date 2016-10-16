from collections import defaultdict
import operator

keywords_file_path = "auto_keywords.txt" # where to write the extracted keywords to
threshold = 0.5 # in what percentage of documents a word must appear to be considered a keyword

#load the data
import json

with open('json_db_all_new.json') as data_file:
    data = json.load(data_file)

relevant_data = [document["text"] for document in data if document["relevancy"] == 1.0]


#Preprocessing of the texts
import nltk
import string

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

def tokenize(text):
    exclude = set(string.punctuation)
    no_punctuation = ''.join(ch for ch in text.lower() if ch not in exclude)

    tokens = no_punctuation.split()
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

    stems = stem_tokens(filtered_tokens, PorterStemmer())

    return stems

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

words_per_doc = map(lambda x: tokenize(x), relevant_data)

def extract_keywords(tokenized_docs):
    """Extracts keywords from the given (preprocessed) documents.

    * extracted keywords are written to a simple text file
    * tokenized_docs ... list of lists, where each inner list contains tokens extracted from one document
    """
    counts = defaultdict(int)
    total_docs = len(tokenized_docs)

    for doc in tokenized_docs:
        dedupl_tokens = set(doc)

        for t in dedupl_tokens:
            counts[t] = counts[t] + 1

    tokens_sorted_by_apps = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)

    keywords = []
    for token, apps in tokens_sorted_by_apps:
        if (apps / float(total_docs)) > threshold:
            keywords.append(token)
        else:
            break

    with open(keywords_file_path, 'w') as f:
        f.write("\n".join(keywords))

def create_keyword_file():
    words_per_doc = map(lambda x: tokenize(x), relevant_data)
    extract_keywords(words_per_doc)
