import streamlit as st
import pandas as pd

# --------- PAGE CONFIGURATION ---------
st.set_page_config(page_title="Harshita's Corner", layout="wide")

# --------- CUSTOM CSS ---------
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; }

    /* Add top margin for Streamlit cloud bar */
    .block-container {
        margin-top: 60px;   /* pushes content down */
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Navigation bar */
    .nav-bar {
        background-color: #f5f5f5;
        display: flex;
        justify-content: center;
        gap: 50px;
        padding: 12px;
        border-bottom: 2px solid #ddd;
        margin-bottom: 30px;
    }
    .nav-bar a {
        text-decoration: none;
        font-weight: 600;
        font-size: 18px;
        color: #222222 !important;
    }
    .nav-bar a.active {
        color: #d62828 !important;
        border-bottom: 3px solid #d62828;
        padding-bottom: 3px;
    }

    /* Card design */
    .card {
        background: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .card h3 { margin: 0; color: #000; }
    .card small { color: #666; }
    .card a { color: #d62828; text-decoration: none; }
    </style>
""", unsafe_allow_html=True)

# --------- LOAD DATA ---------
reviews_df = pd.read_csv("reviews.csv")
insta_df = pd.read_csv("instagram_links.csv")

# --------- NAVIGATION STATE ---------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

pages = ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]

# --------- HEADER ---------
st.markdown("<h1 style='text-align:center; color:#d62828;'>Harshita's Corner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Follow my journey as a DU student sharing movie reviews and music!</p>", unsafe_allow_html=True)

# --------- NAVIGATION BAR ---------
nav_links = []
for page in pages:
    active_class = "active" if st.session_state.current_page == page else ""
    nav_links.append(f"<a href='?page={page}' class='{active_class}'>{page}</a>")

st.markdown(f"<div class='nav-bar'>{''.join(nav_links)}</div>", unsafe_allow_html=True)

# Update current page from query params
current_page = st.query_params.get("page", [st.session_state.current_page])[0]
st.session_state.current_page = current_page

# --------- CONTENT ---------
if current_page == "Home":
    for _, row in reviews_df.iterrows():
        st.markdown(f"""
        <div class='card'>
            <h3>{row['title']} ⭐ {row['rating']}/5</h3>
            <small>{row['date']} | {row['read_time']} min read</small>
            <p>{row['review']}</p>
            <a href='{row['link']}'>Read More</a>
        </div>
        """, unsafe_allow_html=True)

    for _, row in insta_df.iterrows():
        caption = row['caption'] if 'caption' in row else ''
        st.markdown(f"<div class='card'><h3>{caption}</h3></div>", unsafe_allow_html=True)
        embed_html = f"""
            <blockquote class="instagram-media" data-instgrm-permalink="{row['url']}" data-instgrm-version="14" style="margin:auto; max-width:540px;"></blockquote>
            <script async src="//www.instagram.com/embed.js"></script>
        """
        st.components.v1.html(embed_html, height=600, scrolling=True)

elif current_page == "Movie Reviews":
    st.markdown("<h2 style='color:#d62828;'>🎬 Movie Reviews</h2>", unsafe_allow_html=True)
    for _, row in reviews_df.iterrows():
        st.markdown(f"""
        <div class='card'>
            <h3>{row['title']} ⭐ {row['rating']}/5</h3>
            <small>{row['date']} | {row['read_time']} min read</small>
            <p>{row['review']}</p>
            <a href='{row['link']}'>Read More</a>
        </div>
        """, unsafe_allow_html=True)

elif current_page == "Music Posts":
    st.markdown("<h2 style='color:#d62828;'>🎵 Music Posts</h2>", unsafe_allow_html=True)
    for _, row in insta_df.iterrows():
        caption = row['caption'] if 'caption' in row else ''
        st.markdown(f"<div class='card'><h3>{caption}</h3></div>", unsafe_allow_html=True)
        embed_html = f"""
            <blockquote class="instagram-media" data-instgrm-permalink="{row['url']}" data-instgrm-version="14" style="margin:auto; max-width:540px;"></blockquote>
            <script async src="//www.instagram.com/embed.js"></script>
        """
        st.components.v1.html(embed_html, height=600, scrolling=True)

elif current_page == "About":
    st.markdown("<h2 style='color:#d62828;'>About Me</h2>", unsafe_allow_html=True)
    st.write("""
    Hi, I'm **Harshita Kesarwani**, a Delhi University student passionate about singing and movies.
    This blog is where I share my honest reviews, singing journey, and stories from my student life.
    """)

elif current_page == "Contact":
    st.markdown("<h2 style='color:#d62828;'>Contact</h2>", unsafe_allow_html=True)
    st.write("""
    📧 Email: **harshita@example.com**  
    📸 Instagram: [@harshita.music](https://instagram.com/harshita.music)
    """)

