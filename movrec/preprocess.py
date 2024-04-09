import sys
import re
import os
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
    if directors_string == "Unknown":
        return ["unknown"]
    split_directors = re.split("\n|,\n|, |\r| & |Director: | and ", directors_string)
    if len(split_directors) == 1 and split_directors[0] == '':
        return split_directors
    return [s.strip() for s in filter(('').__ne__, split_directors)]

def clean_cast(cast_string):
    if cast_string == "Unknown":
        return ["unknown"]
    split_cast = re.split("\n|,\n|, |\r| & |Cast: | and ", cast_string)
    if len(split_cast) == 1 and split_cast[0] == '':
        return split_cast
    return [s.strip() for s in filter(('').__ne__, split_cast)]

class Preprocessor:
    
    def __init__(self, movies_data):
        # initialize moviesData here
        self.movies_data = pd.read_csv(movies_data)
        self.movies_data.astype('object')

    def clean(self):
        self.movies_data['Genre'] = self.movies_data['Genre'].fillna('unknown')
        self.movies_data['Genre'] = self.movies_data['Genre'].apply(lambda genre: clean_genre(genre))

        self.movies_data['Cast'] = self.movies_data['Cast'].fillna('unknown')
        self.movies_data['Cast'] = self.movies_data['Cast'].apply(lambda cast: clean_cast(cast))

        self.movies_data['Director'] = self.movies_data['Director'].fillna('unknown')
        self.movies_data['Director'] = self.movies_data['Director'].apply(lambda director: clean_directors(director))

    
    def printAll(self):
        # loop through movieids and print id | title \n
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'preprocess_output')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        with open("preprocess_output/titles.csv", 'w') as titles, open("preprocess_output/summaries.csv", 'w') as summaries, open("preprocess_output/fullplot.csv", 'w') as fullplot, open("preprocess_output/other.csv", 'w') as other:
            titles.write("id|title\n")
            summaries.write("id|summary\n")
            fullplot.write("id|fullplot\n")
            other.write("id|genre|release year|director|cast\n")
            for index, row in self.movies_data.iterrows():
                titles.write(f"{index}|{row['Title']}\n")
                summaries.write(f"{index}|{row['PlotSummary']}\n")
                fullplot.write(f"{index}|{row['Plot']}\n")

                other_string = str(index) + "|"

                for index, genre in enumerate(row['Genre']):
                    if index == 0:
                        other_string += genre
                    else:
                        other_string += "," + genre

                other_string += "|" + str(row['Release Year']) + "|"

                for index, director in enumerate(row['Director']):
                    if index == 0:
                        other_string += director
                    else:
                        other_string += ',' + director
                
                other_string += "|"

                for index, cast in enumerate(row['Cast']):
                    if index == 0:
                        other_string += cast
                    else:
                        other_string += ',' + cast

                other.write(other_string+"\n")

def main():
    movies_csv = sys.argv[1]
    p = Preprocessor(movies_csv)
    p.clean()
    p.printAll()

if __name__ == "__main__":
    main()