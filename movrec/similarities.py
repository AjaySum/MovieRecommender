# here we compute similarities based on plot and summary
# add necessary imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
import sys
from torchtext.vocab import Vectors
import nltk
import os
import pickle
nltk.download('punkt')



class SimilarityCalculator():
    fullPlotsDoc = ""
    summariesDoc = ""

    # load in pretrained GloVe for word embeddings
    dir = os.path.join(os.path.dirname(os.getcwd()), "glove.6B")
    wordVectors = Vectors(name=os.path.join(dir, 'glove.6B.300d.txt'))

    fullPlotVecs = {} # id --> full plot embedding vec
    summaryVecs = {} # id --> summary embedding vec


    def __init__(self, fullPlotsDoc, summariesDoc):
        # find doc in directory created by preprocess
        self.fullPlotsDoc = f"preprocess_output/{fullPlotsDoc}"
        self.summariesDoc = f"preprocess_output/{summariesDoc}"
    
    def makeEmbeddings(self):
        with open(self.fullPlotsDoc, 'r') as file:
            # skip the line with schema
            next(file)
            for line in file:
                line = line.strip()
                # clean 
                line = line.replace('"', '')
                # separate id and text
                items = line.split('|')
                # store embedding vector for id
                self.fullPlotVecs[int(items[0])] = self.createEmbeddingVec(items[1])
        with open(self.summariesDoc, 'r') as file:
            # skip the line with schema
            next(file)
            for line in file:
                line = line.strip()
                # clean
                line = line.replace('"', '')
                # separate id and text
                items = line.split('|')
                # store embedding vector for id
                self.summaryVecs[int(items[0])] = self.createEmbeddingVec(items[1])
        
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'similarities_output')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        # create pickle files
        with open('similarities_output/fullPlotEmbeddings.pkl', 'wb') as f:
            # Pickle the full plot dictionary and write it to the file
            pickle.dump(self.fullPlotVecs, f)
        
        with open('similarities_output/summaryEmbeddings.pkl', 'wb') as f:
            # Pickle the summary dictionary and write it to the file
            pickle.dump(self.summaryVecs, f)
        
        


    def createEmbeddingVec(self, text):
        # create tokens
        words = nltk.word_tokenize(text.lower())
        # get word embeddings
        word_embeddings = [self.wordVectors[word].numpy() for word in words if word in self.wordVectors.stoi]
        # return paragraph vector or None if no word embeddings
        if word_embeddings:
            word_embeddings_array = np.array(word_embeddings)
            paragraph_vector = torch.mean(torch.tensor(word_embeddings_array), dim=0)
            return paragraph_vector
        else:
            return None



def main():
    # make an instance of the similarity calculator and pass in the documents with full plot and summary
    # docs should have format id | text
    s = SimilarityCalculator(fullPlotsDoc="fullplot.csv", summariesDoc="summaries.csv")
    s.makeEmbeddings()

if __name__ == "__main__":
    main()