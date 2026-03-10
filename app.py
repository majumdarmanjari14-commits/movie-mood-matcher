import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ── Load your trained model and data ──────────────────────────────────────────
model           = joblib.load('mood_model.pkl')
feature_columns = joblib.load('feature_columns.pkl')
movies_ml       = pd.read_csv('movies_ml.csv')

# ── Mood to emoji map ─────────────────────────────────────────────────────────
mood_emojis = {
    "Happy":      "😄",
    "Sad":        "😢",
    "Scared":     "😱",
    "Excited":    "🤩",
    "Thoughtful": "🤔",
    "Dark":       "🖤",
    "Nostalgic":  "🌅",
}

# ── Keyword to mood map (how text input gets converted to a mood) ──────────────
keyword_mood_map = {
    "happy":      "Happy",
    "joyful":     "Happy",
    "cheerful":   "Happy",
    "good":       "Happy",
    "sad":        "Sad",
    "depressed":  "Sad",
    "heartbroken":"Sad",
    "lonely":     "Sad",
    "scared":     "Scared",
    "anxious":    "Scared",
    "terrified":  "Scared",
    "nervous":    "Scared",
    "excited":    "Excited",
    "hyped":      "Excited",
    "pumped":     "Excited",
    "energetic":  "Excited",
    "thoughtful": "Thoughtful",
    "curious":    "Thoughtful",
    "reflective": "Thoughtful",
    "bored":      "Thoughtful",
    "dark":       "Dark",
    "angry":      "Dark",
    "gloomy":     "Dark",
    "nostalgic":  "Nostalgic",
    "nostalgic":  "Nostalgic",
    "sentimental":"Nostalgic",
    "misty":      "Nostalgic",
}

def text_to_mood(user_input):
    user_input = user_input.lower()
    for keyword, mood in keyword_mood_map.items():
        if keyword in user_input:
            return mood
    return None

def recommend_movies(mood, n=5):
    mood_movies = movies_ml[movies_ml['mood'] == mood]
    return mood_movies['clean_title'].sample(min(n, len(mood_movies))).tolist()

# ── App UI ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Movie Mood Matcher", page_icon="🎬")

st.title("🎬 Movie Mood Matcher")
st.subheader("Tell me how you're feeling — I'll find the perfect movie.")

st.divider()

user_input = st.text_input(
    "How are you feeling right now?",
    placeholder="e.g. I'm feeling nostalgic, a bit sad, excited..."
)

if user_input:
    detected_mood = text_to_mood(user_input)

    if detected_mood:
        emoji = mood_emojis.get(detected_mood, "🎬")
        st.success(f"Mood detected: **{detected_mood}** {emoji}")
        
        st.divider()
        st.subheader(f"🍿 Movies for your {detected_mood} mood:")
        
        recommendations = recommend_movies(detected_mood, n=10)

for i, movie in enumerate(recommendations, 1):
    st.markdown(f"**{i}.** {movie}")

if st.button("🔄 Not satisfied? Get new recommendations"):
    new_recommendations = recommend_movies(detected_mood, n=10)
    st.subheader("🍿 Here's another set:")
    for i, movie in enumerate(new_recommendations, 1):
        st.markdown(f"**{i}.** {movie}")
    else:
        st.warning("Hmm, I didn't catch that mood. Try words like: happy, sad, excited, nostalgic, scared, dark, thoughtful.")

st.divider()
st.caption("Built with ❤️ using Python, scikit-learn & Streamlit")