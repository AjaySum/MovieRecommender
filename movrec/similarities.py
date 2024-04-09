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
nltk.download('punkt')



class SimilarityCalculator():
    fullPlotsDoc = ""
    summariesDoc = ""
    dir = os.path.join(os.path.dirname(os.getcwd()), "glove.6B")
    wordVectors = Vectors(name=os.path.join(dir, 'glove.6B.300d.txt'))

    # key is tuple (id1, id2) and value is similarity score
    summariesSimilarity = {}
    fullPlots = [] # sorted by id
    summaryVecs = {} # sorted by id
    ids = []

    def __init__(self, fullPlotsDoc, summariesDoc):
        self.fullPlotsDoc = fullPlotsDoc
        self.summariesDoc = summariesDoc
    
    def readIn(self):
        with open(self.fullPlotsDoc, 'r') as file:
            for line in file:
                line = line.strip()
                items = line.split('|')
                self.ids.append(items[0])
                self.fullPlots.append(items[1])
                # self.summariesSimilarity[items[0]] = items[1]
        with open(self.summariesDoc, 'r') as file:
            for line in file:
                line = line.strip()
                line = line.replace('"', '')
                items = line.split('|')
                self.summaryVecs[items[0]] = self.createSummaryVec(items[1])


    def createSummaryVec(self, summary):
        words = nltk.word_tokenize(summary.lower())
        word_embeddings = [self.wordVectors[word].numpy() for word in words if word in self.wordVectors.stoi]
        if word_embeddings:
            paragraph_vector = torch.mean(torch.tensor(word_embeddings), dim=0)
            return paragraph_vector
        else:
            return None
    
    # def pad_vector(self, vector, target_length):
    #     if len(vector) < target_length:
    #         padding_length = target_length - len(vector)
    #         padded_vector = np.pad(vector, ((0, padding_length), (0, 0)), mode='constant')
    #         return padded_vector
    #     else:
    #         return vector
    
    def enc_summaries(self):
        out_file = f"summaryEmbeddingScores.txt"
        sys.stdout = open(out_file, 'w')
        for key1, val1 in self.summaryVecs.items():
            for key2, val2 in self.summaryVecs.items():
                if key1 != key2:

                    if val1 is not None and val2 is not None:
                    #     min_length = min(len(val1), len(val2))
                    #     val1 = val1[:min_length]
                    #     val2 = val2[:min_length]
                    #     # Pad vectors to match the maximum length
                    #     # val1 = self.pad_vector(val1, max_length)
                    #     # val2 = self.pad_vector(val2, max_length)

                        val1 = val1.reshape(1, -1)
                        val2 = val2.reshape(1, -1)
                        similarity = max(float(cosine_similarity(val1, val2)[0][0]), 0)
                        print(f"{key1} {key2}|{similarity}") 
                    else:
                        print(f"{key1} {key2}|0") 

        
    def tfIdf_fullPlots(self):
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
    s = SimilarityCalculator("testFullPlots.csv", "testSummaries.csv")
    s.readIn()
    s.enc_summaries()
    s.tfIdf_fullPlots()

if __name__ == "__main__":
    main()