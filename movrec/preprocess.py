import csv
import sys
import re
import nltk
import pandas as pd

# Here we simply process all the text data
# add necessary imports, including dataset
class Movie: 
    def __init__(self):
        self.id = -1
        self.title = ""
        self.genre = []
        self.summary = ""
        self.fullplot = ""
        self.cast = []
        self.directors = []
        self.years = []




genre_frequency = {}

def clean_genre(genre_string):
    global genre_frequency
    split_genre = re.split(", |,|/| /|-", genre_string)
    updated_split_genre = []
    for genre in split_genre:
        if ' ' in genre:
            words = genre.split(' ')
            for word in words:
                updated_split_genre.append(word)
                genre_frequency[word] = genre_frequency.get(word, 0) + 1
        else:
            updated_split_genre.append(genre)
            genre_frequency[genre] = genre_frequency.get(genre, 0) + 1
            
    return [s.strip() for s in filter(('').__ne__, updated_split_genre)]



def clean_directors(directors_string):
    pass


def clean_cast(cast_string):
    split_cast = re.split("\n|,\n|, |\r| & |Cast: | and ", cast_string)
    if len(split_cast) == 1 and split_cast[0] == '':
        return split_cast
    return [s.strip() for s in filter(('').__ne__, split_cast)]

def clean_summary(summary):
    pass

def clean_full_plot(plot):
    pass


class Preprocessor:
    
    def __init__(self, movies_data):
        # initialize moviesData here
        self.movies_data = pd.read_csv(movies_data)
        self.movies_data.astype('object')

    def clean(self):
        self.movies_data['Genre'] = self.movies_data['Genre'].fillna('unknown')
        self.movies_data['Genre'] = self.movies_data['Genre'].apply(lambda genre: clean_genre(genre))

        for key, value in sorted(genre_frequency.items(), key=lambda x:-x[1]):
            print(f"{key}: {value}")

        self.movies_data['Cast'] = self.movies_data['Cast'].fillna('')
        self.movies_data['Cast'] = self.movies_data['Cast'].apply(lambda cast: clean_cast(cast))

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
        # for i in range(10):
        #     self.movies[i] = Movie()
        #     self.movies[i].id = i
        #     self.movies[i].title = f"test{i}"

        # loop through movieids and print id | title \n
        with open("titles.csv", 'w') as titles:
            titles.write("id,title\n")
            for val in self.movies.values():
                titles.write(f"{val.id},{val.title}\n")


        # change stdout to summaries.txt
        # loop through summaries dict and print id | word1 word2 ... \n
        with open("summaries.csv", 'w') as summaries:
            summaries.write("id,summary\n")
            for val in self.movies.values():
                summaries.write(f"{val.id},{val.summary}\n")
    
        # change stdout to fullplots.txt
        # loop through fullplots dict and print id | word1 word2 ... \n
        with open("fullplot.csv", 'w') as fullplot:
            fullplot.write("id,fullplot\n")
            for val in self.movies.values():
                fullplot.write(f"{val.id},{val.fullplot}\n")

        # change stdout to other.txt
        # loop through and print id | year | dir1 dir2 ... | cast1 cast2 ... \n
        with open("other.csv", 'w') as other:
            other.write("id|genres|years|directors|cast\n")
            for val in self.movies.values():
                other.write(f"{val.id}|")
                
                # Write genres
                for i, genre in enumerate(val.genres):
                    if i == 0:
                        other.write(f"{genre}")
                    else:
                        other.write(f",{genre}")
                other.write("|")

                # Write years
                for i, year in enumerate(val.years):
                    if i == 0:
                        other.write(f"{year}")
                    else:
                        other.write(f",{year}")
                other.write("|")

                # Write directors
                for i, director in enumerate(val.directors):
                    if i == 0:
                        other.write(f"{director}")
                    else:
                        other.write(f",{director}")
                other.write("|")

                # Write cast
                for i, cast in enumerate(val.cast):
                    if i == 0:
                        other.write(f"{cast}")
                    else:
                        other.write(f",{cast}")
                other.write("\n")

def main():
    movies_csv = sys.argv[1]
    p = Preprocessor(movies_csv)
    p.clean()

if __name__ == "__main__":
    main()