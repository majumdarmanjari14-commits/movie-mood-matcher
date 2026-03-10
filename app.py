import streamlit as st
import pandas as pd
import joblib
import requests

# ── Load model & data ─────────────────────────────────────────────────────────
model           = joblib.load('mood_model.pkl')
feature_columns = joblib.load('feature_columns.pkl')
movies_ml       = pd.read_csv('movies_ml.csv')

# ── Paste your TMDB API key here ──────────────────────────────────────────────
TMDB_API_KEY = "0ade3e6d9574ed0b3d7e4ad0101ba04a"

# ── Mood config ───────────────────────────────────────────────────────────────
mood_config = {
    "Happy":      {"emoji": "😄", "color": "#F5C518", "bg": "#1a1600"},
    "Sad":        {"emoji": "😢", "color": "#6eb5ff", "bg": "#00101a"},
    "Scared":     {"emoji": "😱", "color": "#ff4444", "bg": "#1a0000"},
    "Excited":    {"emoji": "🤩", "color": "#ff8c00", "bg": "#1a0d00"},
    "Thoughtful": {"emoji": "🤔", "color": "#a78bfa", "bg": "#0d001a"},
    "Dark":       {"emoji": "🖤", "color": "#888888", "bg": "#0a0a0a"},
    "Nostalgic":  {"emoji": "🌅", "color": "#f97316", "bg": "#1a0d00"},
}

keyword_mood_map = {
    "happy":       "Happy",
    "joyful":      "Happy",
    "cheerful":    "Happy",
    "good":        "Happy",
    "sad":         "Sad",
    "depressed":   "Sad",
    "heartbroken": "Sad",
    "lonely":      "Sad",
    "scared":      "Scared",
    "anxious":     "Scared",
    "terrified":   "Scared",
    "nervous":     "Scared",
    "excited":     "Excited",
    "hyped":       "Excited",
    "pumped":      "Excited",
    "energetic":   "Excited",
    "thoughtful":  "Thoughtful",
    "curious":     "Thoughtful",
    "reflective":  "Thoughtful",
    "bored":       "Thoughtful",
    "dark":        "Dark",
    "angry":       "Dark",
    "gloomy":      "Dark",
    "nostalgic":   "Nostalgic",
    "sentimental": "Nostalgic",
    "misty":       "Nostalgic",
}

def text_to_mood(user_input):
    user_input = user_input.lower()
    for keyword, mood in keyword_mood_map.items():
        if keyword in user_input:
            return mood
    return None

def recommend_movies(mood, n=10):
    mood_movies = movies_ml[movies_ml['mood'] == mood]
    return mood_movies['clean_title'].sample(min(n, len(mood_movies))).tolist()

def get_poster(title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
        res = requests.get(url).json()
        results = res.get('results', [])
        if results and results[0].get('poster_path'):
            return f"https://image.tmdb.org/t/p/w300{results[0]['poster_path']}"
    except:
        pass
    return None

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Movie Mood Matcher", page_icon="🎬", layout="wide")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0e0e0e;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #1c1c1c;
        color: white;
        border: 2px solid #333;
        border-radius: 12px;
        padding: 14px 18px;
        font-size: 18px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #e50914;
        box-shadow: 0 0 0 2px rgba(229,9,20,0.3);
    }
    .stButton > button {
        background-color: #e50914;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 15px;
        cursor: pointer;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #b20710;
    }
    .movie-card {
        background: #1c1c1c;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        transition: transform 0.2s;
        height: 100%;
    }
    .movie-card:hover {
        transform: scale(1.03);
    }
    .movie-card img {
        width: 100%;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .movie-card p {
        font-size: 13px;
        font-weight: 600;
        margin: 0;
        color: #ffffffcc;
    }
    .mood-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 20px;
        margin-bottom: 20px;
    }
    .placeholder-poster {
        width: 100%;
        aspect-ratio: 2/3;
        background: #2a2a2a;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center; font-size:48px;'>🎬 Movie Mood Matcher</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#aaa; font-size:18px;'>Tell me how you're feeling — I'll find the perfect movie.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_input = st.text_input("", placeholder="e.g. I'm feeling nostalgic, a bit sad, excited...")

# ── Results ───────────────────────────────────────────────────────────────────
if user_input:
    detected_mood = text_to_mood(user_input)

    if detected_mood:
        config = mood_config[detected_mood]
        color  = config["color"]
        emoji  = config["emoji"]

        st.markdown(f"""
            <div style='text-align:center; margin: 20px 0;'>
                <span class='mood-badge' style='background:{config["bg"]}; color:{color}; border: 2px solid {color};'>
                    {emoji} {detected_mood} Mood
                </span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<h3 style='color:{color}; text-align:center;'>🍿 Movies for your {detected_mood} mood</h3>", unsafe_allow_html=True)

        def show_movies(movies):
            cols = st.columns(5)
            for i, movie in enumerate(movies):
                with cols[i % 5]:
                    poster = get_poster(movie)
                    if poster:
                        st.markdown(f"""
                            <div class='movie-card'>
                                <img src='{poster}' alt='{movie}'/>
                                <p>{movie}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class='movie-card'>
                                <div class='placeholder-poster'>🎬</div>
                                <p>{movie}</p>
                            </div>
                        """, unsafe_allow_html=True)

        recommendations = recommend_movies(detected_mood, n=10)
        show_movies(recommendations)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Show me different movies"):
                new_recommendations = recommend_movies(detected_mood, n=10)
                st.markdown(f"<h3 style='color:{color}; text-align:center;'>🍿 Another set for you</h3>", unsafe_allow_html=True)
                show_movies(new_recommendations)
    else:
        st.warning("Hmm, I didn't catch that mood. Try words like: happy, sad, excited, nostalgic, scared, dark, thoughtful.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555; font-size:13px;'>Built with ❤️ using Python, scikit-learn & Streamlit</p>", unsafe_allow_html=True)

