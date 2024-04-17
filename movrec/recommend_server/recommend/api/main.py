import recommend
import pickle
import math
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
    origin_language = {}

    # key: id2
    fullPlotScores = {}
    summariesScores = {}
    genreScores = {}
    finalScores = {}

    # set weights
    fp_w = 0.26 # full plot weight 
    s_w = 0.37 # summary weight
    d_w = 0.1 # director weight
    c_w = 0.1 # cast weight
    y_w = 0.02 # year weight
    g_w = 0.15 # genre weight
    l_w = 0.05 # language weight
    
    constWeights = {"fp_w": 0.26, "s_w": 0.37, "d_w": 0.1, "c_w": 0.1, "y_w": 0.02, "g_w": 0.15, "l_w": 0.05}

    currLev = {"fp_w": 3, "s_w": 3, "d_w": 3, "c_w": 3, "y_w": 3, "g_w": 3, "l_w": 3}
    
    queryId = -1

    def __init__(self):
        # initialize all docs and queryStr
        self.queryStr = None
        self.queryId = -1
    
    def updateWeights(self):
        self.fp_w = self.constWeights["fp_w"] + (self.currLev["fp_w"] - 3) * 0.15 * self.constWeights["fp_w"]
        self.s_w = self.constWeights["s_w"] + (self.currLev["s_w"] - 3) * 0.15 * self.constWeights["s_w"]
        self.d_w = self.constWeights["d_w"] + (self.currLev["d_w"] - 3) * 0.15 * self.constWeights["d_w"]
        self.c_w = self.constWeights["c_w"] + (self.currLev["c_w"] - 3) * 0.15 * self.constWeights["c_w"]
        self.y_w = self.constWeights["y_w"] + (self.currLev["y_w"] - 3) * 0.15 * self.constWeights["y_w"]
        self.g_w = self.constWeights["g_w"] + (self.currLev["g_w"] - 3) * 0.15 * self.constWeights["g_w"]
        self.l_w = self.constWeights["l_w"] + (self.currLev["l_w"] - 3) * 0.15 * self.constWeights["l_w"]

    def factors(self):
        print("Scoring full plots...")
        self.fullPlotScores = self.encoding(self.fullplot_embeddings)
        print("Scoring summaries...")
        self.summariesScores = self.encoding(self.summary_embeddings)

        for key, fpVal in self.fullPlotScores.items():  
            self.finalScores[key] = (self.fp_w * fpVal) + (self.s_w * self.summariesScores[key])

        self.finalScores = dict(sorted(self.finalScores.items(), key=lambda item: item[1], reverse=True))
        # Get the top 25 items 
        self.finalScores = dict(list(self.finalScores.items())[:25])
        # get cast + director 
        print("Scoring cast and directors...")
        self.castDirectorScoreCalc()
        # get genre
        print("Scoring genres...")
        self.genreScore()
        # get yr
        print("Scoring year...")
        self.yrScoreCalc()
        print("Scoring language...")
        self.languageScore()
        print("Done scoring!")

    def yrScoreCalc(self):
        # penalize based on how far the year is
        for id2 in self.finalScores.keys():
            diff = abs(self.id_year[id2] -self.id_year[self.queryId])
            ans = math.log(1/(diff + 1))
            ans /= math.log(1/117)
            ans *= -1
            self.finalScores[id2] += self.y_w * ans

    def languageScore(self):
        query_language = set(self.origin_language[self.queryId])
        for movie_id in self.finalScores:
            movie_language = set(self.origin_language[movie_id])
            intersection = query_language.intersection(movie_language)
            union = query_language.union(movie_language)
            self.finalScores[movie_id] += self.l_w * (len(intersection) / len(union))


    def castDirectorScoreCalc(self):
        print("Scoring cast and directors...")
        id1Cast = set(self.id_castdirector[self.queryId]['cast'])
        id1Directors = set(self.id_castdirector[self.queryId]['director'])
        for id2 in self.finalScores.keys():
            id2Cast = set(self.id_castdirector[id2]['cast'])
            id2Directors = set(self.id_castdirector[id2]['director'])
            intersectionCast = id1Cast.intersection(id2Cast)
            intersectionDirectors = id1Directors.intersection(id2Directors)
            self.finalScores[id2] += self.c_w * (len(intersectionCast)/len(id1Cast)) + self.d_w * (len(intersectionDirectors)/len(id2Cast))

    def encoding(self, vectorDict):
        answers = {}
        val1 = vectorDict[self.queryId]
        for key2 in self.relevIds.copy():
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
        query_genres = set([x.lower() for x in self.id_genres[self.queryId]])

        for genre, ids in self.genre_ids.items():
            if genre in query_genres or genre == 'unknown':
                for movie_id in ids:
                    self.relevIds.add(movie_id)
                
    def genreScore(self):
        query_genres = set([x.lower() for x in self.id_genres[self.queryId]])
        #update final score based on weights, (global)
        for movie_id in self.finalScores:
            movie_genres = set()
            for genre, ids in self.genre_ids.items():
                if movie_id in ids:
                    movie_genres.add(genre)
        #don't use query genres since can't read
            intersection = query_genres.intersection(movie_genres)
            union = query_genres.union(movie_genres)
            self.finalScores[movie_id] += self.g_w * (len(intersection) / len(union))

    def languageScore(self):
        query_language = set(self.origin_language[self.queryId])
        for movie_id in self.finalScores:
            movie_language = set(self.origin_language[movie_id])
            intersection = query_language.intersection(movie_language)
            union = query_language.union(movie_language)
            self.finalScores[movie_id] += self.l_w * (len(intersection) / len(union))

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
        
        with open('preprocess_output/origin_language.pkl', 'rb') as f:
            self.origin_language = pickle.load(f)


    def calculateScore(self):
        # Should return the top 25
        print("Filtering genres...")
        self.genreFilter()
        
        # Delete query movie from relevIds
        if self.queryId in self.relevIds:
            self.relevIds.remove(self.queryId)
        
        print("Starting scoring...")
        self.factors()
        print("Sorting results...")
        return sorted(self.finalScores.items(), key=lambda x: -x[1])

    def findId(self, query):
        if query in self.name_id:
            self.queryId = self.name_id[query]
            return True
        return False

c = Calculate()