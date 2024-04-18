import pandas as pd
from datasets import load_dataset

movies_dataset = load_dataset("vishnupriyavr/wiki-movie-plots-with-summaries")
train_movies = movies_dataset['train']  

#first panda dataframe, then csv
df = pd.DataFrame(train_movies)
output_csv = "movies_dataset.csv"
df.to_csv(output_csv, index=False)
print(f"CSV data can be seen in: {output_csv}")
