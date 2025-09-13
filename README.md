# Movie Recommender System

## Overview
This project is a Movie Recommendation System that suggests similar movies based on a selected title. It is built using **Streamlit** for the web interface and precomputed movie metadata for generating recommendations.
**Live demo:** [Movie Recommender System](https://movie-recommender-system-arpita.streamlit.app/)

## Dataset
The dataset used for this project has been picked from **Kaggle** and includes:
- **movies.csv**: Contains movie metadata such as movie titles, genres, release dates, and other details.
- **credits.csv**: Contains additional information such as cast and crew for each movie.

## Files
- **app.py**: Main Streamlit application to run the recommender system.
- **main.ipynb**: Jupyter Notebook used for data exploration, preprocessing, and creating the recommendation pipeline.
- **movie_dict.pkl**: Pickled file storing processed movie metadata for fast lookups.
- **requirements.txt**: List of dependencies required to run the project.


## Features
- Select a movie from the dropdown list.
- Get top recommended movies based on similarity.
- Display posters of recommended movies (if available).
