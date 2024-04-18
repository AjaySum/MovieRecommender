# here we compute final few to print
# add necessary imports
import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import math

class Calculate():
    # store only those ids that are not filtered out
    relevIds = set()

    id_name = {}  # id --> name of movie
    name_id = {} # name of movie --> id
    genre_ids = {} # genre --> list of ids
    id_genres = {} # id --> list of genres
    id_castdirector = {} # 2d dict for id --> cast and dir
    id_year = {} # id --> release yr 
    id_summary = {} # id --> summary
    summary_embeddings = {} # id --> summary embeddings
    fullplot_embeddings = {} # id --> full plot embeddings
    origin_language = {} # id --> language

    # key: id2
    fullPlotScores = {}
    summariesScores = {}
    finalScores = {} # will eventually have only top 25 to output

    # current weights
    fp_w = 0.26 # full plot weight 
    s_w = 0.38 # summary weight
    d_w = 0.1 # director weight
    c_w = 0.01 # cast weight
    y_w = 0.05 # year weight
    g_w = 0.3 # genre weight
    l_w = 0.0 # language weight - set to 0 due for current implementation since we filter instead

    # unchanging weights
    constWeights = {"fp_w": 0.36, "s_w": 0.48, "d_w": 0.15, "c_w": 0.05, "y_w": 0.05, "g_w": 0.3, "l_w": 0}

    # current level for weights
    currLev = {"fp_w": 3, "s_w": 3, "d_w": 3, "c_w": 3, "y_w": 3, "g_w": 3, "l_w": 3}
    
    queryId = -1

    def __init__(self):
        # initialize all docs and queryStr
        self.queryStr = None
        self.queryId = -1
        print("Reading in data...")
        self.readIn()

    def updateWeights(self):
        # update weights by 25% of const based on change in level, where 3 is default
        self.s_w = self.constWeights["s_w"] + (self.currLev["s_w"] - 3) * 0.25 * self.constWeights["s_w"]
        self.d_w = self.constWeights["d_w"] + (self.currLev["d_w"] - 3) * 0.25 * self.constWeights["d_w"]
        self.c_w = self.constWeights["c_w"] + (self.currLev["c_w"] - 3) * 0.25 * self.constWeights["c_w"]
        self.y_w = self.constWeights["y_w"] + (self.currLev["y_w"] - 3) * 0.25 * self.constWeights["y_w"]
        self.g_w = self.constWeights["g_w"] + (self.currLev["g_w"] - 3) * 0.25 * self.constWeights["g_w"]
        self.l_w = self.constWeights["l_w"] + (self.currLev["l_w"] - 3) * 0.25 * self.constWeights["l_w"]

    
    def factors(self):
        print("Scoring full plots...")
        self.fullPlotScores = self.encoding(self.fullplot_embeddings)
        print("Scoring summaries...")
        self.summariesScores = self.encoding(self.summary_embeddings)
        # find weighted sum for full plot and summary scores
        for key, fpVal in self.fullPlotScores.items():  
            self.finalScores[key] = (self.fp_w * fpVal) + (self.s_w * self.summariesScores[key])

        # sort by descending
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
        # get language - not used meaningfully with current implementation, but kept in case we change formula
        # print("Scoring language...")
        # self.languageScore()
        print("Done scoring!")


    def yrScoreCalc(self):
        # penalize based on how far the movie 2's year is from query release year
        for id2 in self.finalScores.keys():
            # find abs diff
            diff = abs(self.id_year[id2] - self.id_year[self.queryId])
            # smoothing and normalize
            ans = math.log(1/(diff + 1))
            ans /= math.log(1/117)
            # multiply by -1 to penalize
            ans *= -1
            self.finalScores[id2] += self.y_w * ans

    
    def castDirectorScoreCalc(self):
        print("Scoring cast and directors...")
        id1Cast = set(self.id_castdirector[self.queryId]['cast'])
        id1Directors = set(self.id_castdirector[self.queryId]['director'])
        # find num overlapping with query and normalize with size of query
        for id2 in self.finalScores.keys():
            id2Cast = set(self.id_castdirector[id2]['cast'])
            id2Directors = set(self.id_castdirector[id2]['director'])
            intersectionCast = id1Cast.intersection(id2Cast)
            intersectionDirectors = id1Directors.intersection(id2Directors)
            self.finalScores[id2] += self.c_w * (len(intersectionCast)/len(id1Cast)) + self.d_w * (len(intersectionDirectors)/len(id1Directors))

    def encoding(self, vectorDict):
        # store similarities
        answers = {}
        val1 = vectorDict[self.queryId]
        #  compute cosine similarity
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
        
    def genreLangFilter(self):
        query_genres = set([x.lower() for x in self.id_genres[self.queryId]])
        query_language = set(self.origin_language[self.queryId])

        for genre, ids in self.genre_ids.items():
            # only keep if relev genre
            if genre in query_genres or genre == 'unknown':
                for movie_id in ids:
                    # filter language
                    if set(self.origin_language[movie_id]) == query_language:
                        self.relevIds.add(movie_id)

    def genreScore(self):
        query_genres = set([x.lower() for x in self.id_genres[self.queryId]])
        # update final score based on weights, (global)
        for movie_id in self.finalScores:
            movie_genres = set()
            for genre, ids in self.genre_ids.items():
                if movie_id in ids:
                    movie_genres.add(genre)
            # find jaccard similarity
            intersection = query_genres.intersection(movie_genres)
            union = query_genres.union(movie_genres)
            self.finalScores[movie_id] += self.g_w * (len(intersection) / len(union))

                
    def languageScore(self):
        # 1 or -1 based on which language
        # not used in current weights, but can be changed
        query_language = set(self.origin_language[self.queryId])
        for movie_id in self.finalScores:
            movie_language = set(self.origin_language[movie_id])
            if query_language == movie_language:
                self.finalScores[movie_id] += self.l_w * 1
            else:
                self.finalScores[movie_id] += self.l_w * -1

 
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
        self.genreLangFilter()
        
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

    def weightPrompter(self):
        print("Weights are between 1-5, with 1 being the lowest and 5 being the highest.")
        print("You can increase or decrease the weight of any factor relative to all other factors.")
        print("Here are the current weights")
        print(f"Full Plot weight: {self.currLev['fp_w']}")
        print(f"Summary weight: {self.currLev['s_w']}")
        print(f"Director weight: {self.currLev['d_w']}")
        print(f"Cast weight: {self.currLev['c_w']}")
        print(f"Year weight: {self.currLev['fp_w']}")
        print(f"Genre weight: {self.currLev['g_w']}")
        # language weight not used in curr implementation
        # print(f"Language weight: {self.currLev['l_w']}")
        inp = 'x'
        while (inp != 'y' and inp != 'n'):
            inp = input("Do you want to adjust weights? (Y/N) ").strip().lower()
            if (inp != 'y' and inp != 'n'):
                print("Invalid input") 
        if (inp == 'y'):
            inp = input("Enter new 'Full Plot' weight between 1-5, or press any other character to skip: ")
            if (inp.isdigit() and int(inp) > 0 and int(inp) < 6):
                self.currLev["fp_w"] = int(inp)
            inp = input("Enter new 'Summary' weight between 1-5, or press any other character to skip: ")
            if (inp.isdigit() and int(inp) > 0 and int(inp) < 6):
                self.currLev["s_w"] = int(inp)
            inp = input("Enter new 'Director' weight between 1-5, or press any other character to skip: ")
            if (inp.isdigit() and int(inp) > 0 and int(inp) < 6):
                self.currLev["d_w"] = int(inp)
            inp = input("Enter new 'Cast' weight between 1-5, or press any other character to skip: ")
            if (inp.isdigit() and int(inp) > 0 and int(inp) < 6):
                self.currLev["c_w"] = int(inp)
            inp = input("Enter new 'Year' weight between 1-5, or press any other character to skip: ")
            if (inp.isdigit() and int(inp) > 0 and int(inp) < 6):
                self.currLev["y_w"] = int(inp)
            inp = input("Enter new 'Genre' weight between 1-5, or press any other character to skip: ")
            if (inp.isdigit() and int(inp) > 0 and int(inp) < 6):
                self.currLev["g_w"] = int(inp)
            # language weight not used in curr implementation
            # inp = input("Enter new 'Language' weight between 1-5, or press any other character to skip: ")
            # if (inp.isdigit() and int(inp) > 0 and int(inp) < 6):
            #     self.currLev["l_w"] = int(inp)
            self.updateWeights()
        return
            

def main():
    # Test with beauty and the beast
    c = Calculate() # add parameters
    while True:
        endPrompt = '-'
        while endPrompt != 'm' and endPrompt != 'x':
            endPrompt = input("Enter 'm' to get a movie recommendation, 'w' to adjust weights, and 'x' to exit: ")
            if endPrompt == 'w':
                c.weightPrompter()
            elif endPrompt != 'm' and endPrompt != 'x':
                print("Invalid Input")


        if endPrompt == 'x':
            print("Thanks for using our recommender!")
            return()

        movieName = input("Enter a movie name to find recommendations for: ").strip()
        if not c.findId(movieName):
            print("Invalid Movie Name")
            continue
        top25 = c.calculateScore()
        
        next5 = 0
        for id, score in top25:
            # print 5 at a time
            if next5 < 5:
                print(f"{id} {c.id_name[id]}: {score}\n{c.id_summary[id]}\n")
                next5 += 1
            else:
                getMore = 'x'
                while getMore != 'y' and getMore != 'n':
                    getMore = input("Do you want 5 more suggestions? (Y/N) ").strip().lower()
                if getMore == 'y':
                    next5 = 0
                else:
                    break


if __name__ == "__main__":
    main()
