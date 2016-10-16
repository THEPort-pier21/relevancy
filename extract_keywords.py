from collections import defaultdict
import operator

keywords_file_path = "auto_keywords.txt" # where to write the extracted keywords to
threshold = 0.7 # in what percentage of documents a word must appear to be considered a keyword

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
