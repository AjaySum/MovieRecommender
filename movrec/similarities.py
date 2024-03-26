# here we compute similarities based on plot and summary
# add necessary imports

class SimilarityCalculator():
    idsDoc = ""
    fullPlotsDoc = ""
    summariesDoc = ""
    ids = set()

    # key is tuple (id1, id2) and value is similarity score
    fullplotsSimilarity = {}
    summariesSimilarity = {}

    def __init__(self, idsDoc, fullPlotsDoc, summariesDoc):
        self.idsDoc = idsDoc
        self.fullPlotsDoc = fullPlotsDoc
        self.summariesDoc = summariesDoc
    
    def readIn(self):
        # open idsDoc and read in values
        # open fullPlotsDoc and read in values
        # open summariesDoc and read in values
        pass

    def enc_summaries(self):
        # loop through all ids
            # loop through all ids minus curr id
                # use a library to find encoding similarity score 
                # store score in summariesSimilarity
        pass
        
    def tfIdf_fullPlots(self):
        # loop through all ids
            # loop through all ids minus curr id
                # use a library to find tfidf score 
                # store score in fullPlotsSimilarity
        pass

    def printAll(self):
        # change stdout to summaries_scores.txt
        # loop through all summariesSimilarity items and print id1 id2 | score

        # change stdout to fullplots_scores.txt
        # loop through all fullPlotsSimilarity items and print id1 id2 | score
        pass


def main():
    s = SimilarityCalculator("ids.txt", "fullplots.txt", "summaries.txt")
    s.readIn()
    s.enc_summaries()
    s.tfIdf_fullPlots()
    s.printAll()

if __name__ == "__main__":
    main()