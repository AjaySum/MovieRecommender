# here we compute final few to print
# add necessary imports

class Calculate():
    idsDoc = ""
    titlesDoc = ""
    fullplotsDoc = ""
    summariesDoc = ""
    otherDoc = ""
    fullPlotScoresDoc = ""
    summariesScoresDoc = ""

    ids = set()

    relevIds = set()

    id_to_title = {}
    title_to_id = {}

    genres = {} # val is set of genres

    cast = {} # val is list of actors
    dirs = {} # val is list of directors
    years = {} # val is numbers

    summaries = {} # val is list of words

    # key: (id1, id2)
    fullPlotScores = {}
    summariesScores = {}
    firstHalfScores = {}
    secondHalfScores = {}
    finalScores = {}

    queryStr = ""
    queryId = -1
    keywords = []



    def __init__(self, queryStr, idsDoc, titlesDoc, summariesDoc, otherDoc, fullPlotScoresDoc, summariesScoresDoc):
        # initialize all docs and queryStr
        self.currId = -1
        pass

    def secondHalf(self):
        # THEY HAD US IN THE FIRST HALF NGL

        # set weights
        d_w = 0 # director weight
        c_w = 0 # cast weight
        y_w = 0 # year weight

        # loop through all relevIds, self.queryId
            # calculate score and save to secondHalfScores
        pass

    def firstHalf(self):
        # THEY HAD US IN THE FIRST HALF NGL

        # set weights
        fp_w = 0.2
        s_w = 0.8

        # loop through all relevIds, self.queryId
            # calculate score based on fullPlotScores and summariesScores and save to firstHalfScores
        pass
    
    def finalCalcAndPrint():
        # set weights
        w_1 = 0
        w_2 = 0
        w_3 = 0 # used for query similarity keywords
        # do jaccard or tfidf to get query keywords similarity to summary
        # loop through all relevIds, self.queryId
            # calculate final score save to finalScores
        
        # find top 5 final scores and output them with score for each part? and maybe which keywords match (if any) - might need more logic
            
        pass


    def genreFilter():
        # filter based on genres. keep all unknowns and add all filtered to relevIds
        pass

    def readIn(self):
        # read in data into the dictionaries
        # compute queryId using Jaccard
        # preprocess keywords in query
        pass

def main():
    c = Calculate() # add parameters
    c.readIn()
    c.genreFilter()
    c.firstHalf()
    c.secondHalf()
    c.finalCalcAndPrint()


if __name__ == "__main__":
    main()