import streamlit as st
import pandas as pd

# --- page config ---
st.set_page_config(page_title="Harshita's Corner", layout="wide")

# --- styling ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
    :root {
        --purple:#6a1b9a;
        --bg:#ffffff;
        --card:#f5f5f7;
        --radius:12px;
        --shadow:0 8px 30px rgba(0,0,0,0.05);
        font-family: 'Inter', system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
    }
    .stApp { background: var(--bg); color:#111; }
    .block-container {
        padding-top: 60px;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1180px;
        margin: auto;
    }
    .site-header {
        text-align: center;
        margin-bottom: 10px;
    }
    .site-header h1 {
        margin: 0;
        font-size: 3rem;
        color: var(--purple);
        line-height: 1.1;
    }
    .site-header p {
        margin: 4px 0 24px;
        font-size: 1rem;
        color: #444;
    }
    .tab-bar {
        display: flex;
        gap: 30px;
        justify-content: center;
        padding: 12px 0;
        border-bottom: 1px solid #e3e3e5;
        margin-bottom: 40px;
    }
    .tab-btn {
        background: none;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        position: relative;
        color: #222;
        border-radius: 6px;
        transition: background .15s;
    }
    .tab-btn:hover { background: rgba(106,27,154,0.05); }
    .tab-btn.active {
        color: var(--purple);
    }
    .tab-btn.active::after {
        content:'';
        position: absolute;
        left:0;
        right:0;
        bottom: -1px;
        height:3px;
        background: var(--purple);
        border-radius: 2px;
    }
    .card {
        background: var(--card);
        padding: 18px 22px;
        border-radius: var(--radius);
        margin-bottom: 24px;
        box-shadow: var(--shadow);
    }
    .card h3 {
        margin: 0 0 6px;
        font-size: 1.5rem;
        color: var(--purple);
    }
    .meta {
        font-size: 12px;
        color: #555;
        margin-bottom: 8px;
    }
    .read-more {
        display: inline-block;
        margin-top: 6px;
        font-weight: 600;
        color: var(--purple);
        text-decoration: none;
    }
    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 16px;
        color: var(--purple);
    }
    .about-box, .contact-box {
        background: var(--card);
        padding: 20px 24px;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        max-width: 900px;
        margin: auto;
    }
    .pill {
        background: var(--purple);
        color: white;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        display: inline-block;
        margin-right: 6px;
    }
    a { text-decoration: none; }
    </style>
""", unsafe_allow_html=True)

# --- data load with fallback ---
try:
    reviews_df = pd.read_csv("reviews.csv")
except FileNotFoundError:
    reviews_df = pd.DataFrame(columns=["title", "review", "rating", "date", "read_time", "link"])

try:
    insta_df = pd.read_csv("instagram_links.csv")
except FileNotFoundError:
    insta_df = pd.DataFrame(columns=["caption", "url"])

# --- navigation state ---
if "tab" not in st.session_state:
    st.session_state.tab = "Home"

# header
st.markdown("<div class='site-header'>"
            "<h1>Harshita's Corner</h1>"
            "<p>Follow my journey as a DU student sharing movie reviews and music!</p>"
            "</div>", unsafe_allow_html=True)

# tabs
tabs = ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]
cols = st.columns(len(tabs))
for i, t in enumerate(tabs):
    is_active = st.session_state.tab == t
    btn = cols[i].button(t, key=f"tab_{t}")
    if btn:
        st.session_state.tab = t

# underline active manually (alternative to CSS class since using button)
st.markdown(f"<div class='tab-bar'>"
            + "".join([
                f"<div style='position:relative;'><span style='font-weight:600; font-size:16px; color:{'var(--purple)' if st.session_state.tab==t else '#222'}; padding:8px 16px;'>{t}</span>"
                + (f"<div style='height:3px; background:var(--purple); border-radius:2px; position:absolute; bottom:-1px; left:0; right:0;'></div>" if st.session_state.tab==t else "")
                + "</div>"
                for t in tabs
            ]) +
            "</div>", unsafe_allow_html=True)

# content switch
if st.session_state.tab == "Home":
    # two-column layout: left reviews, right music
    left, right = st.columns([2, 1])
    with left:
        st.markdown("<div class='section-title'>Latest Movie Reviews</div>", unsafe_allow_html=True)
        if reviews_df.empty:
            st.info("No movie reviews yet.")
        else:
            for _, row in reviews_df.iterrows():
                title = row.get("title", "")
                rating = row.get("rating", "")
                date = row.get("date", "")
                read_time = row.get("read_time", "")
                review_text = row.get("review", "")
                link = row.get("link", "#")
                st.markdown(f"""
                    <div class='card'>
                        <div class='meta'>{date} | {read_time} min read</div>
                        <h3>{title} ⭐ {rating}/5</h3>
                        <p style='margin:8px 0 0; color:#222;'>{review_text}</p>
                        <a class='read-more' href='{link}' target='_blank'>Read More →</a>
                    </div>
                """, unsafe_allow_html=True)
    with right:
        st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
        if insta_df.empty:
            st.info("No music posts yet.")
        else:
            for _, row in insta_df.iterrows():
                caption = row.get("caption", "")
                url = row.get("url", "")
                st.markdown(f"<div class='card'><div class='pill'>🎵</div><h3 style='display:inline-block; margin:0;'>{caption}</h3></div>", unsafe_allow_html=True)
                embed_html = f"""
                    <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:400px;"></blockquote>
                    <script async src="//www.instagram.com/embed.js"></script>
                """
                st.components.v1.html(embed_html, height=500, scrolling=True)

elif st.session_state.tab == "Movie Reviews":
    st.markdown("<div class='section-title'>Movie Reviews</div>", unsafe_allow_html=True)
    if reviews_df.empty:
        st.info("No movie reviews yet.")
    else:
        for _, row in reviews_df.iterrows():
            title = row.get("title", "")
            rating = row.get("rating", "")
            date = row.get("date", "")
            read_time = row.get("read_time", "")
            review_text = row.get("review", "")
            link = row.get("link", "#")
            st.markdown(f"""
                <div class='card'>
                    <div class='meta'>{date} | {read_time} min read</div>
                    <h3>{title} ⭐ {rating}/5</h3>
                    <p style='margin:8px 0 0; color:#222;'>{review_text}</p>
                    <a class='read-more' href='{link}' target='_blank'>Read More →</a>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.tab == "Music Posts":
    st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
    if insta_df.empty:
        st.info("No music posts yet.")
    else:
        for _, row in insta_df.iterrows():
            caption = row.get("caption", "")
            url = row.get("url", "")
            st.markdown(f"<div class='card'><div class='pill'>🎵</div><h3 style='display:inline-block; margin:0;'>{caption}</h3></div>", unsafe_allow_html=True)
            embed_html = f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:500px;"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
            """
            st.components.v1.html(embed_html, height=500, scrolling=True)

elif st.session_state.tab == "About":
    st.markdown("<div class='section-title'>About Me</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="about-box">
            <p>Hi, I'm <strong>Harshita Kesarwani</strong>, a Delhi University student passionate about singing and movies. This blog is my space to share honest movie reviews, musical experiments, and slices from student life. I aim to connect with people who care about authenticity and storytelling.</p>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.tab == "Contact":
    st.markdown("<div class='section-title'>Contact</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="contact-box">
            <p>📧 <strong>Email:</strong> <a href="mailto:harshita@example.com">harshita@example.com</a></p>
            <p>📸 <strong>Instagram:</strong> <a href="https://instagram.com/harshita.music" target="_blank">@harshita.music</a></p>
        </div>
    """, unsafe_allow_html=True)
