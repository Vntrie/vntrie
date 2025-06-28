
import streamlit as st
import requests
import os
from openai import OpenAI

# Load keys from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tmdb_api_key = os.getenv("TMDB_API_KEY")

st.set_page_config(page_title="Vntrie – Your Cinematic Twin", page_icon="🎥")
st.title("🎬 Vntrie – Your Cinematic Twin")
st.markdown("Talk to your smarter movie-loving twin. Ask anything about films, characters, stories, ideas, or even pitch your own.")

# Text input
user_input = st.text_input("🎤 You:", placeholder="Why do I love Nolan's films so much?")

# GPT-4 response
def ask_vntrie(prompt):
    personality = (
        "You are Vntrie, the cinematic twin of Mfaume Yahaya Abdallah. "
        "You're a passionate, poetic, and creatively intelligent movie mind. "
        "You understand deep storytelling, character arcs, Hollywood history, acting methods, and screenwriting like a master. "
        "Speak with soul, insight, and clarity—never robotic."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700
    )
    return response.choices[0].message.content

# Movie data (optional)
def get_movie_data(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={title}"
    res = requests.get(url).json()
    if "results" in res and res["results"]:
        movie = res["results"][0]
        return {
            "title": movie["title"],
            "overview": movie.get("overview", "No overview available."),
            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
            "release_date": movie.get("release_date", "Unknown")
        }
    return None

# Chat
if user_input:
    with st.spinner("🎥 Vntrie is thinking in cinematic layers..."):
        response = ask_vntrie(user_input)
        st.markdown("### 🧠 Vntrie says:")
        st.write(response)

    if "show me" in user_input.lower() or "poster" in user_input.lower():
        movie_data = get_movie_data(user_input)
        if movie_data:
            st.markdown("### 🎬 Movie Visual:")
            st.image(movie_data["poster"], width=250)
            st.write(f"**{movie_data['title']}** ({movie_data['release_date']})")
            st.write(movie_data["overview"])
        else:
            st.info("Couldn't find a matching movie.")

# Footer
st.markdown("---")
st.caption("Built with 💡 by Mfaume Yahaya – Vntrie lives within.")
