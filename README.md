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

## Getting Started: Quick Instructions

For a quick setup, follow these steps:

1. Install pre-trained word embeddings glove.6B from Stanford here: [glove.6B dataset](https://nlp.stanford.edu/data/glove.6B.zip). Move the unzipped directory to `eecs486-MovieRecommender/`.
2. Run `./runall_cli.sh` for command-line interface, or `./runall_ui.sh` for GUI (access from [localhost:8000](http://localhost:8000))

## Detailed Instructions: Manual Setup
### Step 1: Initial Setup
  - Install the Stanford Glove.6B Word Embeddings here: [glove.6B dataset](https://nlp.stanford.edu/data/glove.6B.zip). Unzip this directory to `eecs486-MovieRecommender/`.
  - Then, we create the virtual environment and download the required libraries. To do this, run `cd movrec` and run `python3 -m venv env` to create the environment. Then run `source env/bin/activate` to activate the environment and run `pip install -r requirements.txt`.
  - Then, we have to install the dataset. To do this, run `python3 dataset.py`.
      - `dataset.py`: Python script that uses the huggingface datasets library to download the Wikipedia Plot Data dataset.

### Step 2: Install the Dataset
-  From the root (`eecs486-MovieRecommender/`), run `cd movrec` and then run `python3 dataset.py
    - `preprocess.py`:
    - `similarities.py`:

