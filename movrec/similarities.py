# here we compute similarities based on plot and summary
# add necessary imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
import sys
from torchtext.vocab import Vectors
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import os
import pickle
nltk.download('punkt')



class SimilarityCalculator():
    fullPlotsDoc = ""
    summariesDoc = ""
    dir = os.path.join(os.path.dirname(os.getcwd()), "glove.6B")
    wordVectors = Vectors(name=os.path.join(dir, 'glove.6B.300d.txt'))

    # key is tuple (id1, id2) and value is similarity score
    summariesSimilarity = {}
    fullPlotSimilarity = {}
    fullPlotVecs = {} # sorted by id
    summaryVecs = {} # sorted by id
    fullPlots = []

    ids = []

    def __init__(self, fullPlotsDoc, summariesDoc):
        self.fullPlotsDoc = f"preprocess_output/{fullPlotsDoc}"
        self.summariesDoc = f"preprocess_output/{summariesDoc}"
    
    def makeEmbeddings(self):
        with open(self.fullPlotsDoc, 'r') as file:
            next(file)
            for line in file:
                line = line.strip()
                items = line.split('|')
                self.ids.append(items[0])
                self.fullPlotVecs[items[0]] = self.createEmbeddingVec(items[1])
        with open(self.summariesDoc, 'r') as file:
            next(file)
            for line in file:
                line = line.strip()
                line = line.replace('"', '')
                items = line.split('|')
                self.summaryVecs[items[0]] = self.createEmbeddingVec(items[1])
        with open('fullPlotEmbeddings.pkl', 'wb') as f:
            # Pickle the dictionary and write it to the file
            pickle.dump(self.fullPlotVecs, f)
        
        with open('summaryEmbeddings.pkl', 'wb') as f:
            # Pickle the dictionary and write it to the file
            pickle.dump(self.summaryVecs, f)
        
        


    def createEmbeddingVec(self, text):
        words = nltk.word_tokenize(text.lower())
        word_embeddings = [self.wordVectors[word].numpy() for word in words if word in self.wordVectors.stoi]
        if word_embeddings:
            word_embeddings_array = np.array(word_embeddings)
            paragraph_vector = torch.mean(torch.tensor(word_embeddings_array), dim=0)
            return paragraph_vector
        else:
            return None
    

    def enc(self, vector, key1):
        answers = {}
        out_file = f"summaryEmbeddingScores.txt"
        sys.stdout = open(out_file, 'w')
        val1 = vector[key1]
        for key2, val2 in vector.items():
            if key1 != key2:
                if val1 is not None and val2 is not None:

                    val1 = val1.reshape(1, -1)
                    val2 = val2.reshape(1, -1)
                    similarity = max(float(cosine_similarity(val1, val2)[0][0]), 0)
                    answers[(key1, key2)] = similarity
                    # print(f"{key1} {key2}|{similarity}") 
                else:
                    answers[(key1, key2)] = 0
                    # print(f"{key1} {key2}|0") 
        return answers
        

        
    def tfIdf(self):
        out_file = f"fullPlotTfIdfScores.txt"
        sys.stdout = open(out_file, 'w')
        # for item in self.summaries:
        #     print(item)
        tfidf_vectorizer = TfidfVectorizer()

        # Fit and transform the documents
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.fullPlots)

        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Print the cosine similarity matrix
        for index, value in np.ndenumerate(cosine_sim):
            if index[0] != index[1]:
                index = str(index)
                index = index.replace("(", "")
                index = index.replace(")", "")
                index = index.replace(",", "")
                value = max(float(value), 0)
                
                print(f"{index}|{value}")



def main():
    s = SimilarityCalculator(fullPlotsDoc="fullplot.csv", summariesDoc="summaries.csv")
    s.makeEmbeddings()

if __name__ == "__main__":
    main()