import streamlit as st
import pickle
import pandas as pd
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import os
import gdown

def download_similarity():
    file_id = "1p5SZ9wZ4poUrQbL_kSuw4HxV5aJC2WcO"
    url = f"https://drive.google.com/uc?id=1p5SZ9wZ4poUrQbL_kSuw4HxV5aJC2WcO"
    output = "similarity.pkl"
    if not os.path.exists(output):
        with st.spinner("Downloading similarity matrix... Please wait."):
            gdown.download(url, output, quiet=False)

download_similarity()

def fetch_poster(movie_id, retries=3, delay=1):
    """
    Fetch movie poster from TMDB with retry logic.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=fbf30cb7ca561e03563dbba43de248a8&language=en-US"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if 'poster_path' in data and data['poster_path']:
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed for movie_id {movie_id}: {e}")
            time.sleep(delay)
    # fallback
    return "https://via.placeholder.com/500x750.png?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    movie_ids = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_ids.append(movie_id)

    # fetch posters in parallel
    with ThreadPoolExecutor() as executor:
        recommended_movies_posters = list(executor.map(fetch_poster, movie_ids))

    return recommended_movies, recommended_movies_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Select Movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
