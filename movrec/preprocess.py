import sys
import re
import os
import pickle
import pandas as pd

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
    
        self.movies_data['Plot'] = self.movies_data['Plot'].fillna('unknown')
        self.movies_data['Plot'] = self.movies_data['Plot'].apply(lambda plot: plot.replace("\n", " ").replace("\r", " "))

        self.movies_data['PlotSummary'] = self.movies_data['PlotSummary'].fillna('unknown')
        self.movies_data['PlotSummary'] = self.movies_data['PlotSummary'].apply(lambda summary: summary.replace("\n", " ").replace("\r", " "))


    def storeAll(self):
        # loop through movieids and print id | title \n
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'preprocess_output')

        name_id = {}
        genre_ids = {}
        id_cast_director = {}
        id_year = {}
        # id_rating = {}

        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        with open("preprocess_output/summaries.csv", 'w') as summaries, open("preprocess_output/fullplot.csv", 'w') as fullplot:
            summaries.write("id|summary\n")
            fullplot.write("id|fullplot\n")
            for index, row in self.movies_data.iterrows():
                summaries.write(f"{index}|{row['PlotSummary']}\n")
                fullplot.write(f"{index}|{row['Plot']}\n")

                name_id[row['Title']] = index
                
                for genre in row['Genre']:
                    if genre not in genre_ids:
                        genre_ids[genre] = []
                    genre_ids[genre].append(index)
                
                id_cast_director[index] = {"cast":[], "director":[]}
                id_cast_director[index]['cast'] = row['Cast']
                id_cast_director[index]['director'] = row['Director']

                id_year[index] = row['Release Year']

        # Save each dict to pickle
        with open('preprocess_output/name_id.pkl', 'wb') as pickle_file:
            pickle.dump(name_id, pickle_file)
        
        with open('preprocess_output/genre_id.pkl', 'wb') as pickle_file:
            pickle.dump(genre_ids, pickle_file)

        with open('preprocess_output/id_castdirector.pkl', 'wb') as pickle_file:
            pickle.dump(id_cast_director, pickle_file)
        
        with open('preprocess_output/id_year.pkl', 'wb') as pickle_file:
            pickle.dump(id_year, pickle_file)


def main():
    movies_csv = sys.argv[1]
    p = Preprocessor(movies_csv)
    p.clean()
    p.storeAll()


if __name__ == "__main__":
    main()