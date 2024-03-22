import sys
import string
import nltk
from nltk.corpus import stopwords
from datasets import load_dataset
movies = load_dataset("vishnupriyavr/wiki-movie-plots-with-summaries")
nltk.download('stopwords')

def clean_movie_text(text):
    punctuation_string = string.punctuation + "…"
    stop_words = set(stopwords.words('english'))

    cleaned_content = []
    for line in text:
        clean_line = ''
        for char in line:
            if char == '’' or char == "'":
                clean_line += "'"
            elif char not in punctuation_string:
                clean_line += char
        cleaned_tokens = [word.lower() for word in clean_line.split() if word.lower() not in stop_words]
        cleaned_content.append(' '.join(cleaned_tokens))

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

