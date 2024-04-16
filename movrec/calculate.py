# here we compute final few to print
# add necessary imports
import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity

class Calculate():
    relevIds = set()

    id_name = {}
    name_id = {}
    genre_ids = {}
    id_genres = {}
    id_castdirector = {}
    id_year = {}
    id_summary = {}
    summary_embeddings = {}
    fullplot_embeddings = {}

    # key: id2
    fullPlotScores = {}
    summariesScores = {}
    genreScores = {}
    finalScores = {}

    # set weights
    fp_w = 0.25 # full plot weight 
    s_w = 0.35 # summary weight
    d_w = 0.1 # director weight
    c_w = 0.1 # cast weight
    y_w = 0.05 # year weight
    g_w = 0.15 # genre weight
    
    
    
    queryId = -1

    def __init__(self):
        # initialize all docs and queryStr
        self.queryStr = None
        self.queryId = -1
        self.readIn()

    def factors(self):



        self.fullPlotScores = self.encoding(self.fullplot_embeddings)
        self.summariesScores = self.encoding(self.summary_embeddings)
        for key, fpVal in self.fullPlotScores:  
            self.finalScores[key] = (self.fp_w * fpVal) + (self.s_w * self.summariesScores[key])
        

        self.finalScores = dict(sorted(self.finalScores.items(), key=lambda item: item[1], reverse=True))
        # Get the top 25 items 
        self.finalScores = dict(list(self.finalScores.items())[:25])
        # get cast + director 
        # get genre
        # get yr


    def castDirectorScoreCalc(self):
        id1Cast = set(self.id_castdirector['cast'][self.queryId])
        id1Directors = set(self.id_castdirector['director'][self.queryId])
        for id2 in self.finalScores.keys():
            id2Cast = set(self.id_castdirector[id2])
            id2Directors = set(self.id_castdirector['director'][id2])
            intersectionCast = id1Cast.intersection(id2Cast)
            direc
            self.finalScores[id2] += self.c_w * (len(intersectionCast)/len(id1Cast))




    def encoding(self, vectorDict):
        answers = {}
        val1 = vectorDict[self.queryId]
        for key2 in self.relevIds:
            val2 = vectorDict[key2]
            if val1 is not None and val2 is not None:
                val1 = val1.reshape(1, -1)
                val2 = val2.reshape(1, -1)
                similarity = max(float(cosine_similarity(val1, val2)[0][0]), 0)
                answers[key2] = similarity
            else:
                answers[key2] = 0
        return answers 
        
    def genreFilter(self):
        # filter based on genres. keep all unknowns and add all filtered to relevIds
        query_genres = set(self.id_genres[self.queryId].lower().split)

        for genre, ids in self.genres.items():
            if genre in query_genres or genre == 'unknown':
                for movie_id in ids:
                    self.relevIds.add(movie_id)
                
    def genreScore(self):
        #update final score based on weights, (global)
        for movie_id in self.finalScores:
            movie_genres = set()
            for genre, ids in self.genres.items():
                if movie_id in ids:
                    movie_genres.add(genre)
        #don't use query genres since can't read
            intersection = query_genres.intersection(movie_genres)
            union = query_genres.union(movie_genres)
            len(intersection) / len(union)
            #self.genreScores[movie_id] = 0 if len(union)


    def readIn(self):
        # read in data into the dictionaries
        with open('preprocess_output/genre_ids.pkl', 'rb') as f:
            self.genre_ids = pickle.load(f)
        
        with open('preprocess_output/id_castdirector.pkl', 'rb') as f:
            self.id_castdirector = pickle.load(f)
        
        with open('preprocess_output/id_genres.pkl', 'rb') as f:
            self.id_genres = pickle.load(f)
        
        with open('preprocess_output/id_name.pkl', 'rb') as f:
            self.id_name = pickle.load(f)
        
        with open('preprocess_output/id_year.pkl', 'rb') as f:
            self.id_year = pickle.load(f)
        
        with open('preprocess_output/name_id.pkl', 'rb') as f:
            self.name_id = pickle.load(f)
        
        with open('preprocess_output/id_summary.pkl', 'rb') as f:
            self.id_summary = pickle.load(f)
        
        with open('similarities_output/summaryEmbeddings.pkl', 'rb') as f:
            self.summary_embeddings = pickle.load(f)
        
        with open('similarities_output/fullPlotEmbeddings.pkl', 'rb') as f:
            self.fullplot_embeddings = pickle.load(f)


    def calculateScore(self):
        # Should return the top 25
        self.genreFilter()
        
        # Delete query movie from relevIds
        if self.queryId in self.relevIds:
            del self.relevIds[self.queryId]    
        finalScores

    
    def findId(self, query):
        if query in self.name_id:
            self.queryId = self.name_id[query]
            return True
        return False
        
def main():
    # Test with beauty and the beast
    c = Calculate() # add parameters
    endFlag = False
    while not endFlag:
        movieName = input("Enter a movie name to find recommendations for: ")
        if not c.findId(movieName):
            print("Invalid Movie Name")
            continue
        top25 = c.calculateScore()
        
        getMore = input("Do you want 5 more suggestions:")
        
        #print(next 5 rank)
        
        
    # c.calculate("Beauty and the Beast")


if __name__ == "__main__":
    main()