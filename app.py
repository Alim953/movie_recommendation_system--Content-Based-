import streamlit as st
import pandas as pd
import requests
import os
import requests
import pickle


st.title('🎬 Movie Recommendation System')

# Load data
df = pd.read_csv('Movies.csv')
movies_list = df.title.values



MODEL_URL = "https://drive.google.com/uc?export=download&id=1lf1oggaP4PBnHMvF42NqPOfQDhrVkCqr"
MODEL_PATH = "similarity.pkl"

# === Download the model if not already there ===
if not os.path.exists(MODEL_PATH):
    st.info("Downloading model from Google Drive...")
    r = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)
    st.success("Model downloaded successfully!")

# === Load the model ===
with open(MODEL_PATH, "rb") as f:
    similarity = pickle.load(f)


# TMDb API key
api_key = '41423f29ec2f9ac44fefef087afbdb8f'

@st.cache_data(show_spinner=False)
def fetch_poster(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    response = requests.get(url)
    data = response.json()

    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/200x300?text=No+Image"


import numpy as np

def recomand(x):
    idx = df[df['title'] == x].index[0]
    sim_scores = similarity[idx]
    top_indices = np.argsort(sim_scores)[-6:-1][::-1]

    recomanded_movies, recommended_posters = [], []
    for i in top_indices:
        movie_name = df.iloc[i].title
        recomanded_movies.append(movie_name)
        recommended_posters.append(fetch_poster(movie_name))

    return recomanded_movies, recommended_posters


option = st.selectbox('Select a movie you like:', movies_list)

if st.button('Recommend'):
    st.subheader('🎥 Recommended Movies:')
    mo, po = recomand(option)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(po[i], caption=mo[i], use_container_width=True)







