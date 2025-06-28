
import streamlit as st
import openai
import requests
import os

# Set API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
tmdb_api_key = os.getenv("TMDB_API_KEY")

st.set_page_config(page_title="Vntrie - Your Movie Genius", page_icon="🎬")

st.title("🎬 Vntrie - Your Personal Movie Genius")
st.markdown("Ask me anything about movies, characters, stories, genres, or recommendations!")

user_query = st.text_input("🎤 Ask Vntrie:", "")

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Vntrie, a film-savvy assistant with 10000 IQ. You love movies, story analysis, character depth, and cinematic trivia. Be detailed and creative."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def get_movie_data(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={title}"
    res = requests.get(url).json()
    if res["results"]:
        movie = res["results"][0]
        return {
            "title": movie["title"],
            "overview": movie.get("overview", "No overview available."),
            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
            "release_date": movie.get("release_date", "Unknown")
        }
    return None

if user_query:
    if "recommend" in user_query.lower() or "movie" in user_query.lower():
        st.write("🧠 Thinking like a movie genius...")
        answer = ask_openai(user_query)
        st.markdown("### 🎞️ Vntrie's Take:")
        st.write(answer)
    else:
        movie_data = get_movie_data(user_query)
        if movie_data:
            st.image(movie_data["poster"], width=250)
            st.markdown(f"**🎬 {movie_data['title']}**")
            st.markdown(f"🗓️ Released: {movie_data['release_date']}")
            st.markdown(f"📝 {movie_data['overview']}")
        else:
            st.write("No results found on TMDb. Here's what I know:")
            st.write(ask_openai(user_query))
