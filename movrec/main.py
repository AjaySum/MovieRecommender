import utils
from datasets import load_dataset
movies = load_dataset("vishnupriyavr/wiki-movie-plots-with-summaries")
import sys
import string


def clean_movie_text(text):
    punctuation_string = string.punctuation + "…"

   
    cleaned_content = []
    for line in text:
        clean_line = ''
        for char in line:
            if char == '’' or char == "'":
                clean_line += "'"
            elif char not in punctuation_string:
                clean_line += char
        cleaned_content.append(clean_line.lower())

    return cleaned_content

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    
    file_path = sys.argv[1]
    movies_dataset = load_dataset(file_path)
    cleaned_movies = []
    for movie in movies_dataset:
        cleaned_movie = clean_movie_text(movie)
        cleaned_movies.append(cleaned_movie)

    print("CLEANED MOVIES: ", cleaned_movies)
