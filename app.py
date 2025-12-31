import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ccd628b548f579c2ec440499fb364936'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/original"+data['poster_path']

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    movie_poster=[]
    for i in movie_list:
        moive_ido=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_poster.append(fetch_poster(moive_ido))

    return recommended_movies,movie_poster

st.title("🎥 Movie Recommendation System")
st.write("Select a movie and get similar recommendations!")

selected_movie = st.selectbox(
    "Choose a movie:",
    movies['title'].values
)

if st.button("Recommend"):
    recommendations,poster = recommend(selected_movie)

    st.subheader("🍿 Recommended Movies")
    

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(poster[i], use_container_width=True)
            st.caption(recommendations[i])
    
