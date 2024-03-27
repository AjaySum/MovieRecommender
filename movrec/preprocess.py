# Here we simply process all the text data
# add necessary imports, including dataset
class Movie: 
    def __init__(self):
        self.id = -1
        self.title = ""
        self.genre = ""
        self.summary = ""
        self.fullplot = ""
        self.cast = []
        self.directors = []
        self.years = []


class Preprocessor:
    
    def __init__(self, moviesData):
        # initialize moviesData here
        self.moviesData = moviesData
        self.movies = {}

    def clean(self):
        # i = 0 start movie id
        # while loop till reading data done
            # add to movieIds
            # add title as string
            # add year after converting to int
            # clean genre, cast and dirs manually and add
            # clean summary, fullplot using library
            # manually make sure there is no '|' character (use as separator later)
            # increment i
        pass
    
    def printAll(self):
        # change stdout to titles.txt
        with open("titles.csv", 'w') as titles:
            self.movies.map(lambda x: f"{x.id},{x.title}")
        # loop through movieids and print id | title \n

        # change stdout to summaries.txt
        # loop through summaries dict and print id | word1 word2 ... \n

        # change stdout to fullplots.txt
        # loop through fullplots dict and print id | word1 word2 ... \n

        # change stdout to other.txt
        # loop through and print id | year | dir1 dir2 ... | cast1 cast2 ... \n
        pass


def main():
    p = Preprocessor()
    p.clean()
    p.printAll()

if __name__ == "__main__":
    main()