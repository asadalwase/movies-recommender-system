import streamlit as st
import pandas as pd
import pickle
import requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=72721b8664f74a57af30ada9fb8f7d69&language=en-US"
    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        st.warning(f"Could not fetch poster for {movie_id}: {e}")
    return "https://via.placeholder.com/500x750?text=No+Poster"



def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id  # ✅ now fetching real movie_id from dataframe
            recommended_movies.append(movies.iloc[i[0]].title)

            # fetch poster from API

            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommendation System')


selected_movie_name = st.selectbox(
"How would you like to be contacted?",
movies['title'].values)

if st.button("Recommend"):
    names,posters = recommendations = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])

