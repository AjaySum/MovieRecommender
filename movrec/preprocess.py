import sys
import re
import os
import pickle
import pandas as pd

genre_frequency = {}

def clean_genre(genre_string):
    # Clean and split genres, updating frequencies
    global genre_frequency
    split_genre = re.split(", |,|/| /|-", genre_string)
    updated_split_genre = []
    # Split each genre name into unique words and append to genre list
    for genre in split_genre:
        if ' ' in genre:
            words = genre.split(' ')
            for word in words:
                updated_split_genre.append(word)
                genre_frequency[word] = genre_frequency.get(word, 0) + 1
        else:
            # Append genre names that do not contain spaces
            updated_split_genre.append(genre)
            genre_frequency[genre] = genre_frequency.get(genre, 0) + 1
            
    return [s.strip() for s in filter(('').__ne__, updated_split_genre)]


# Function to clean the director strings.
def clean_directors(directors_string):
    if directors_string == "Unknown":
        return ["unknown"]
    
    # Split director string on delimeters
    split_directors = re.split("\n|,\n|, |\r| & |Director: | and ", directors_string)
    
    # If there are no directors, then return the string
    if len(split_directors) == 1 and split_directors[0] == '':
        return split_directors
    
    # Otherwise, strip the strings and filter out the empty strings.
    return [s.strip() for s in filter(('').__ne__, split_directors)]


# Function to clean the cast strings.
def clean_cast(cast_string):
    if cast_string == "Unknown":
        return ["unknown"]
    
    # Split cast string on delimeters.
    split_cast = re.split("\n|,\n|, |\r| & |Cast: | and ", cast_string)

    # If there is no cast, then return the string.
    if len(split_cast) == 1 and split_cast[0] == '':
        return split_cast
    
    # Otherwise, strip the strings and filter out the empty strings.
    return [s.strip() for s in filter(('').__ne__, split_cast)]


# Clean the origin language string.
def clean_language(language_string):
    # Replace underscores with spaces and split on the ", " delimeter.
    return language_string.replace('_', ' ').split(', ')


class Preprocessor:
    
    def __init__(self, movies_data):
        # Read in the movies dataset.
        self.movies_data = pd.read_csv(movies_data)
        self.movies_data.astype('object')
        self.origin_language = {}

    # Function that cleans the pandas dataframe.
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

        self.movies_data['Origin/Ethnicity'] = self.movies_data['Origin/Ethnicity'].fillna('unknown')
        self.movies_data['Origin/Ethnicity'] = self.movies_data['Origin/Ethnicity'].apply(lambda language: clean_language(language))
        
        for index, row in self.movies_data.iterrows():
            self.origin_language[index] = row['Origin/Ethnicity']


    # Function to write to output dictionaries and csv files.
    def storeAll(self):
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'preprocess_output')

        name_id = {}
        id_name = {}
        id_genres = {}
        genre_ids = {}
        id_cast_director = {}
        id_year = {}
        id_summary = {}
        # id_rating = {}

        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        # Open csv files.
        with open("preprocess_output/summaries.csv", 'w') as summaries, open("preprocess_output/fullplot.csv", 'w') as fullplot:
            summaries.write("id|summary\n")
            fullplot.write("id|fullplot\n")
            for index, row in self.movies_data.iterrows():

                # Write to plot and summaries.
                summaries.write(f"{index}|{row['PlotSummary']}\n")
                fullplot.write(f"{index}|{row['Plot']}\n")

                # Store data in dictionaries
                name = row['Title']
                if name in name_id:
                    name += f" ({row['Release Year']})"

                name_id[name] = index
                id_name[index] = name
                
                id_genres[index] = row['Genre']

                for genre in row['Genre']:
                    if genre not in genre_ids:
                        genre_ids[genre] = []
                    genre_ids[genre].append(index)
                
                id_cast_director[index] = {"cast":[], "director":[]}
                id_cast_director[index]['cast'] = row['Cast']
                id_cast_director[index]['director'] = row['Director']

                id_year[index] = row['Release Year']

                id_summary[index] = row['PlotSummary']

        # Save each dict to pickle
        with open('preprocess_output/name_id.pkl', 'wb') as pickle_file:
            pickle.dump(name_id, pickle_file)

        with open('preprocess_output/id_name.pkl', 'wb') as pickle_file:
            pickle.dump(id_name, pickle_file)

        with open('preprocess_output/id_genres.pkl', 'wb') as pickle_file:
            pickle.dump(id_genres, pickle_file)
        
        with open('preprocess_output/genre_ids.pkl', 'wb') as pickle_file:
            pickle.dump(genre_ids, pickle_file)

        with open('preprocess_output/id_castdirector.pkl', 'wb') as pickle_file:
            pickle.dump(id_cast_director, pickle_file)
        
        with open('preprocess_output/id_year.pkl', 'wb') as pickle_file:
            pickle.dump(id_year, pickle_file)
        
        with open('preprocess_output/id_summary.pkl', 'wb') as pickle_file:
            pickle.dump(id_summary, pickle_file)

        with open('preprocess_output/origin_language.pkl', 'wb') as pickle_file:
            pickle.dump(self.origin_language, pickle_file)

        with open('preprocess_output/origin_language.txt', 'w') as txt_file:
            txt_file.write("id|origin_language\n")
            for index, language in self.origin_language.items():
                txt_file.write(f"{index}|{language}\n")

def main():
    movies_csv = sys.argv[1]
    p = Preprocessor(movies_csv)
    p.clean()
    p.storeAll()
    with open('top_genres.txt', 'w') as f:
        for genre, freq in sorted(genre_frequency.items(), key= lambda x: -x[1]):
            f.write(f"{genre} {freq}\n")

if __name__ == "__main__":
    main()