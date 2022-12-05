import pandas as pd
from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import os

nowPath = os.getcwd()

df = pd.read_csv(nowPath + "/2017_songs/data.csv")

feature_cols=['acousticness', 'danceability', 'duration_ms', 'energy',
              'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
              'speechiness', 'tempo', 'time_signature', 'valence',]

scaler = MinMaxScaler()
normalized_df = scaler.fit_transform(df[feature_cols])


# Create a pandas series with song titles as indices and indices as series values
indices = pd.Series(df.index, index=df['song_title']).drop_duplicates()

# Create cosine similarity matrix based on given matrix
cosine = cosine_similarity(normalized_df)

def generate_recommendation(song_title, model_tyoe=cosine):
    """
    Purpose: Function for song recommendations
    Inputs: song title and type of similarity model
    Output: Pandas series of recommended songs
    """
    # Get song indices
    index = indices[song_title]
    # Get list of songs for given songs
    score = list(enumerate(model_tyoe[indices['Parallel Lines']]))
    # Sort the most similar songs
    similarity_score = sorted(score, key=lambda x:x[1], reverse=True)
    # Select the top10 recommend songs
    similarity_score = similarity_score[1:11]
    top_sons_index = [i[0] for i in similarity_score]
    # Top10 recommend songs
    top_songs = df['song_title'].iloc[top_sons_index]
    return top_songs

#print("Recommended Songs:")
#print(generate_recommendation('Parallel Lines', cosine).values)


# Create sigmoid kernel matrix based on given matrix
#sig_kernel = sigmoid_kernel(normalized_df)
#print("Recommended Songs:")
#print(generate_recommendation('Parallel Lines', sig_kernel).values)
