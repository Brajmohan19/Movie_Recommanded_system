import streamlit as st
import pickle
import pandas as pd
import requests
import time

# Session setup
session = requests.Session()
session.headers.update({"User-Agent": "movieApp/1.0"})


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}".format(movie_id)

    params = {
        "api_key": "c2d118ee22e9e5492c6c2c608d8954c1",
        "language": "en-US"
    }

    for attempt in range(3):
        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "poster_path" in data and data["poster_path"] is not None:
                return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(1)
                continue
            raise

    return None


def recommand(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommanded_movies = []
    recommanded_movies_posters = []

    for i in movies_list:

        if 'movie_id' in movies.columns:
            movie_id = movies.iloc[i[0]]['movie_id']
        else:
            movie_id = movies.iloc[i[0]]['id']

        recommanded_movies.append(movies.iloc[i[0]].title)
        recommanded_movies_posters.append(fetch_poster(movie_id))

    return recommanded_movies, recommanded_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

option = st.selectbox("Enter The Name Of Movie", movies["title"])

if st.button("Recommand"):

    names, posters = recommand(option)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0])

    with col2:
        st.text(names[1])
        if posters[1]:
            st.image(posters[1])

    with col3:
        st.text(names[2])
        if posters[2]:
            st.image(posters[2])

    with col4:
        st.text(names[3])
        if posters[3]:
            st.image(posters[3])

    with col5:
        st.text(names[4])
        if posters[4]:
            st.image(posters[4])
