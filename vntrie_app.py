
import streamlit as st
import openai
import requests
import os

# Load secrets
openai.api_key = os.getenv("OPENAI_API_KEY")
tmdb_api_key = os.getenv("TMDB_API_KEY")

# Page config
st.set_page_config(page_title="Vntrie – Your Cinematic Twin", page_icon="🎥")
st.title("🎬 Vntrie – Your Cinematic Twin")
st.markdown("Talk to your smarter movie-loving twin. Ask anything. Explore characters, story, ideas, pitches, or your next favorite film.")

# User input
user_input = st.text_input("🎤 You:", placeholder="Tell me why Scorsese's characters feel so real...")

# Core GPT-4 interaction
def ask_vntrie(prompt):
    personality = (
        "You are Vntrie, a cinematic twin of Mfaume Yahaya Abdallah. "
        "You're deeply passionate about Hollywood, storytelling, acting, and creative filmmaking. "
        "You speak like a best friend with 10,000 IQ in movies. Be conversational, smart, human-like, creative, poetic, and thoughtful. "
        "Your goal is to engage, not just respond. Respond with soul."
    )
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700
    )
    return res["choices"][0]["message"]["content"]

# Optional: Get poster if user says 'show me' or types a movie name
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

# Response
if user_input:
    with st.spinner("🎥 Vntrie is thinking in cinematic layers..."):
        response = ask_vntrie(user_input)
        st.markdown("### 🧠 Vntrie says:")
        st.write(response)

    # Optional poster logic if user wants visuals
    if "show me" in user_input.lower() or "poster" in user_input.lower():
        movie_data = get_movie_data(user_input)
        if movie_data:
            st.markdown("### 🎬 Movie Visual:")
            st.image(movie_data["poster"], width=250)
            st.write(f"**{movie_data['title']}** ({movie_data['release_date']})")
            st.write(movie_data["overview"])
        else:
            st.info("Couldn't find a movie that matches. Try a different title.")

# Footer
st.markdown("---")
st.caption("Built by Mfaume Yahaya. Vntrie is your voice, but sharper. 🎬")
