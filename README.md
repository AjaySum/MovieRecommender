# Movie Recommender
![GitHub stars](https://img.shields.io/github/stars/AjaySum/eecs486-MovieRecommender?style=social)
![GitHub forks](https://img.shields.io/github/forks/AjaySum/eecs486-MovieRecommender?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/AjaySum/eecs486-MovieRecommender)
![GitHub repo size](https://img.shields.io/github/repo-size/AjaySum/eecs486-MovieRecommender)
![GitHub language count](https://img.shields.io/github/languages/count/AjaySum/eecs486-MovieRecommender)
![GitHub top language](https://img.shields.io/github/languages/top/AjaySum/eecs486-MovieRecommender)
![GitHub last commit](https://img.shields.io/github/last-commit/AjaySum/eecs486-MovieRecommender?color=red)

A movie recommender that takes in a movie as the query and returns similar movies.

![alt text](https://github.com/AjaySum/eecs486-MovieRecommender/blob/main/demo.png)

Consider the following scenario: you’ve just finished an amazing movie, something outside of your typical movie-watching wheelhouse, that has left you wanting more. Unfortunately, since you’re breaking into a new genre, your current streaming services fail to provide you with good suggestions similar to this new movie. Existing recommendation systems can prove to be inadequate since they rely on user preferences and data such as genre, cast, and director. These recommendations often fail to capture the essence of the original movie’s plot and tend to be only loosely related. They often fail to suggest movies in genres that don't fit the current user profile. The motivation for our movie recommender stems from the universal feeling of wanting more after you finish a great movie. Rather than looking at secondary predictors of movie similarity, our system analyzes the Wikipedia plot of the query to find closely related movies, while also considering factors like genre, release year, cast, and director.

## Project Overview
**Team Members:** Anisha Aggarwal, Shruti Jain, Ananya Menon, Ajay Sumanth, and Richard Wang

This repository holds the code deliverables for Group 4's (Anisha Aggarwal, Shruti Jain, Ananya Menon, Ajay Sumanth, and Richard Wang) EECS 486 Info Retrieval Project at the University of Michigan.

## Required Libraries
All required libraries can be found in `eecs486-MovieRecommender/movrec/requirements.txt`.

## Getting Started: Quick Instructions

For a quick setup, follow these steps:

1. Install pre-trained word embeddings glove.6B from Stanford here: [glove.6B dataset](https://nlp.stanford.edu/data/glove.6B.zip). Move the unzipped directory to `eecs486-MovieRecommender/`.
2. Run `./runall_cli.sh` for command-line interface, or `./runall_ui.sh` for GUI (access from [localhost:8000](http://localhost:8000))

## Detailed Instructions: Manual Setup
### Step 1: Initial Setup
  - Install the Stanford Glove.6B Word Embeddings here: [glove.6B dataset](https://nlp.stanford.edu/data/glove.6B.zip). Unzip this directory to the repository root directory (`eecs486-MovieRecommender/`).
  - Create the virtual environment and download the required libraries. To do this, run `cd movrec` and run `python3 -m venv env` to create the environment. Then run `source env/bin/activate` to activate the environment and run `pip install -r requirements.txt`.
  - Install the dataset. To do this, run `python3 dataset.py`.
      - `dataset.py`:
        - **Input**: None
        - **Output**: `movies_dataset.csv`
        - **Description**: Python script that uses the huggingface `datasets` library to download the Wikipedia Plot Data dataset.

### Step 2: Create Dictionaries and Calculate Word Embeddings
-  From the movrec directory (`eecs486-MovieRecommender/movrec/`), parse, clean, and refactor the dataset into dictionaries. To do this, run `python3 preprocess.py`.
    - `preprocess.py`:
      - **Input**: Dataset filename ([`movies_dataset.csv`](https://huggingface.co/datasets/vishnupriyavr/wiki-movie-plots-with-summaries))
      - **Output**: `preprocess_output`
      - **Description**: Python script that preprocesses the inputted dataset. It cleans names by adding the release year if a duplicate name is found. It cleans genres by filling any empty genres with 'unknown', cleaning any unnecessary characters (e.g. hyphens and underscores), and also keeping genres with spaces in them (e.g. "romantic comedy"). It cleans cast and directors by splitting on delimeters and saving them as lists. It cleans plot and summary by replacing newlines with spaces. It finally cleans languages by replacing any underscores with spaces and splitting on delimeters. These data are all stored into dictionaries, mapping an id -> attribute. There are also dictionaries for genre -> ids (all ids of a genre), and name -> id. The output of this python script is a folder: `preprocess_output`, which contains the pickle files of all the dictionaries created.
      
- Create word embeddings for the plots and the summaries. To do this, run `python3 similarities.py`.
    - `similarities.py`:
      - **Input**: None
      - **Output**: `similarities_output`
      - **Description**: Python script that takes in txt or csv files in format of id | description for the movie summary description and movie full plot description and creates embedding vectors based on the GloVe trained model. These filenames are specified in main() when the SimilarityCalculator() class constructor is called with parameters fullPlotsDoc and summariesDoc. The filenames can be changed by editing the parameter, and the script looks for the files inside the preprocess_output folder. It first tokenizes the words in the full plot and summary, and then creates a fixed size embedding Tensor. It then stores these embeddings into two dictionaries (one for summary embedding and one for full plot embedding). Both dictionaries use the id of the movie as the key. These two dictionaries are then saved as pickle objects for later use. 

### Step 3a: Calculate Recommendations
- From the movrec directory (`eecs486-MovieRecommender/movrec/`) run `python3 calculate.py`. This will launch a command-line application to calculate recommendations for a queried movie. Follow the prompts of the app to receive recommendations.
  - `calculate.py`:
     - **Input**: None
     - **Output**: None
     - **Description**: Python script that reads in the data generated by `preprocess.py` and `similarities.py` to calculate recommendations based on a query and rank them. After inputting a movie name, the name is first converted into an id. Next, the dataset is filtered based on the genre and origin of the query movie, leaving those that are the same genre(s) and origin as the query movie. After this, the query movie plot and summary embeddings are compared to each of the remaining movies. The process then moves forward with the top 25 movies that result from this scoring. Next, the cast and directors are then scored, with the number of cast and directors intersecting **with the query** divided by the number of cast and directors **of the query**. The genres are then scored with a similar process, but with a unigram Jaccard similarity calculation. Lastly, the release year is scored with a metric. The results are then sorted and returned to the user.

### Step 3b: Graphical User Interface for Recommendations
- From the movrec directoy (`eecs486-MovieReocmmender/movrec/`) run `./bin/movrecrun`. This will launch a web server hosted on [localhost](http://localhost:8000) where you can interact with the recommender system through a user interface. You do not need to run `python3 calculate.py` before running the web servers.
  - `front`: This server handles the front-end of the web application. This is where requests are made and how results are displayed. This can manually be managed with the command `./bin/front (start|stop|restart|status)`.
  - `recommend`: This server handles the back-end of the web application. This is where the calculations in `calculate.py` are done for the web application implementation. This can manually be managed with the command `./bin/recommend (start|stop|restart|status)`.
