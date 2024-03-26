# Here we simply process all the text data
# add necessary imports, including dataset

class Preprocessor:
    moviesData = "" # will store loaded dataset, will change type
    movieIds = set()

    # all dictionaries below indexed with id

    titles = {} # val is plain string
    genres = {} # val is set of genres
    summaries = {} # val is list of words
    fullplots = {} # val is list of words
    cast = {} # val is list of actors
    dirs = {} # val is list of directors
    years = {} # val is numbers
    
    def __init__(self):
        # initialize moviesData here
        pass

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
        # change stdout to ids.txt
        # loop through movieids and print id \n

        # change stdout to titles.txt
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