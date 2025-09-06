import pickle
import streamlit as st
import requests

# ✅ Your OMDb API Key
OMDB_API_KEY = "e5f91d6d"

# Load movie data and similarity matrix
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Function to fetch poster using OMDb API
def fetch_poster(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        data = requests.get(url).json()
        poster_url = data.get('Poster')
        if poster_url and poster_url != "N/A":
            return poster_url
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:  # Top 5 similar movies
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movies.iloc[i[0]].title))

    return recommended_movies, recommended_posters

# Streamlit UI configuration
st.set_page_config(page_title="Premium Movie Recommender", layout="wide")

# Custom CSS for stylish premium dark interface
st.markdown("""
<style>
/* Dark gradient background */
body {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
    color: #ffffff;
}

/* Premium stylish heading */
h1 {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 3rem;
    color: #222222; /* Dark stylish heading */
    text-align: center;
    letter-spacing: 2px;
    text-shadow: 2px 2px 5px rgba(255,255,255,0.15), -2px -2px 5px rgba(0,0,0,0.7);
    background: rgba(0,0,0,0.3);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
    margin-bottom: 2rem;
}

/* Glassmorphism movie cards */
.movie-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 15px;
    text-align: center;
    color: #fff;
    box-shadow: 0 8px 32px 0 rgba(0,0,0,0.7);
    backdrop-filter: blur(10px);
    transition: transform 0.3s, box-shadow 0.3s;
    margin-bottom: 20px;
}

.movie-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 40px 0 rgba(0,0,0,0.9);
}

/* Movie title */
.movie-title {
    font-weight: bold;
    margin-top: 10px;
    font-size: 1.1rem;
    color: #e0e0e0;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(to right, #434343, #1c1c1c);
    color: white;
    font-size: 1.1rem;
    font-weight: bold;
    border-radius: 12px;
    padding: 0.5rem 1.5rem;
    box-shadow: 2px 2px 15px rgba(0,0,0,0.6);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 4px 4px 25px rgba(0,0,0,0.8);
}

/* Selectbox styling */
.css-1cpxqw2, .css-1q1n0ol {
    font-size: 1.2rem;
    color: #fff;
    background-color: rgba(0,0,0,0.4);
    border-radius: 8px;
}

/* Image styling */
img {
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.8);
}
</style>
""", unsafe_allow_html=True)

# Page title
st.title("🎬 Movie Recommender System")

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie:", movie_list)

# Show recommendations
if st.button("Show Recommendations"):
    recommended_movies, recommended_posters = recommend(selected_movie)

    if recommended_movies:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{recommended_posters[idx]}" width="150"/>
                    <div class="movie-title">{recommended_movies[idx]}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No recommendations found.")
