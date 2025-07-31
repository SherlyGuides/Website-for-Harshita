import streamlit as st
import pandas as pd
from urllib.parse import urlencode

# --- config ---
st.set_page_config(page_title="Harshita's Corner", layout="wide")

# --- styling (soft purple theme, high contrast) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --purple:#9f7aea;
    --purple-dark:#6e3cb0;
    --bg:#fafaff;
    --card:#ffffff;
    --radius:12px;
    --shadow:0 20px 50px -10px rgba(159,122,234,0.15);
    font-family: 'Inter', system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
}
body, .stApp { background: var(--bg); color: #1f1f28; }
.block-container {
    padding-top: 80px;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1120px;
    margin: auto;
}
.site-header {
    text-align: center;
    margin-bottom: 12px;
    padding: 35px 20px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(159,122,234,0.15) 0%, rgba(255,255,255,1) 80%);
    color: #1f1f28;
    position: relative;
}
.site-header h1 {
    margin: 0;
    font-size: 2.8rem;
    line-height: 1.05;
    font-weight: 700;
    color: var(--purple-dark);
}
.site-header p {
    margin: 6px 0 0;
    font-size: 1rem;
    color: #444;
}
.tab-bar {
    display: flex;
    justify-content: center;
    gap: 22px;
    flex-wrap: wrap;
    margin: 28px 0 36px;
    padding: 4px 8px;
    background: #f5f3fc;
    border-radius: 999px;
}
.tab {
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 14px;
    text-decoration: none;
    color: #4a4a63;
    transition: all .15s;
    position: relative;
}
.tab:hover {
    background: rgba(159,122,234,0.08);
}
.tab.active {
    background: var(--purple);
    color: white;
    box-shadow: 0 12px 35px -5px rgba(159,122,234,0.35);
}
.card {
    background: var(--card);
    padding: 18px 22px;
    border-radius: var(--radius);
    margin-bottom: 22px;
    box-shadow: var(--shadow);
    border: 1px solid rgba(159,122,234,0.1);
}
.card h3 {
    margin: 0 0 6px;
    font-size: 1.5rem;
    color: var(--purple-dark);
}
.meta {
    font-size: 12px;
    color: #555;
    margin-bottom: 6px;
}
.read-more {
    display: inline-block;
    margin-top: 6px;
    font-weight: 600;
    color: var(--purple-dark);
    text-decoration: none;
}
.section-title {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 14px;
    color: var(--purple-dark);
}
.info-box {
    background: #ffffff;
    padding: 22px 26px;
    border-radius: var(--radius);
    box-shadow: 0 20px 40px -10px rgba(159,122,234,0.08);
    margin-bottom: 30px;
    border: 3px solid var(--purple);
    color: #1f1f28;
}
.info-box h2 {
    margin-top: 0;
    color: var(--purple-dark);
}
.info-box p {
    margin: 0.5rem 0;
    font-size: 1rem;
    line-height: 1.45;
}
.info-box a {
    color: var(--purple-dark);
    font-weight: 600;
    text-decoration: none;
}
.pill {
    display: inline-block;
    background: var(--purple);
    color: white;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 8px;
}
</style>
""", unsafe_allow_html=True)

# --- data load ---
try:
    reviews_df = pd.read_csv("reviews.csv")
except:
    reviews_df = pd.DataFrame(columns=["title","review","rating","date","read_time","link"])
try:
    insta_df = pd.read_csv("instagram_links.csv")
except:
    insta_df = pd.DataFrame(columns=["caption","url"])

# --- tab state from query param fallback to session ---
params = st.experimental_get_query_params()
tab = params.get("tab", [st.session_state.get("tab", "Home")])[0]
if tab not in ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]:
    tab = "Home"
st.session_state["tab"] = tab

# --- header ---
st.markdown("""
    <div class="site-header">
        <h1>Harshita's Corner</h1>
        <p>Follow my journey as a DU student sharing movie reviews and music!</p>
    </div>
""", unsafe_allow_html=True)

# --- tab bar as HTML links ---
def make_link(label):
    base = st.get_url_params()
    # build new query param
    q = {"tab": label}
    href = "?" + urlencode(q)
    cls = "tab active" if st.session_state["tab"] == label else "tab"
    return f"<a class='{cls}' href='{href}'>{label}</a>"

tabs_html = "<div class='tab-bar'>" + "".join([make_link(l) for l in ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]]) + "</div>"
st.markdown(tabs_html, unsafe_allow_html=True)

# --- content ---
current = st.session_state["tab"]

if current == "Home":
    left, right = st.columns([2,1], gap="large")
    with left:
        st.markdown("<div class='section-title'>Latest Movie Reviews</div>", unsafe_allow_html=True)
        if reviews_df.empty:
            st.info("No movie reviews yet.")
        else:
            for _, r in reviews_df.iterrows():
                title = r.get("title","")
                rating = r.get("rating","")
                date = r.get("date","")
                read_time = r.get("read_time","")
                review_text = r.get("review","")
                link = r.get("link","#")
                st.markdown(f"""
                    <div class="card">
                        <div class="meta">{date} | {read_time} min read</div>
                        <h3>{title} ⭐ {rating}/5</h3>
                        <p style="margin:6px 0 0;">{review_text}</p>
                        <a class="read-more" href="{link}" target="_blank">Read More →</a>
                    </div>
                """, unsafe_allow_html=True)
    with right:
        st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
        if insta_df.empty:
            st.info("No music posts yet.")
        else:
            for _, r in insta_df.iterrows():
                caption = r.get("caption","")
                url = r.get("url","")
                st.markdown(f"""
                    <div class="card">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <div class="pill">🎵</div>
                            <div><h3 style="margin:0; font-size:1.25rem;">{caption}</h3></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                embed_html = f"""
                    <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
                    <script async src="//www.instagram.com/embed.js"></script>
                """
                st.components.v1.html(embed_html, height=450, scrolling=True)

elif current == "Movie Reviews":
    st.markdown("<div class='section-title'>Movie Reviews</div>", unsafe_allow_html=True)
    if reviews_df.empty:
        st.info("No movie reviews yet.")
    else:
        for _, r in reviews_df.iterrows():
            title = r.get("title","")
            rating = r.get("rating","")
            date = r.get("date","")
            read_time = r.get("read_time","")
            review_text = r.get("review","")
            link = r.get("link","#")
            st.markdown(f"""
                <div class="card">
                    <div class="meta">{date} | {read_time} min read</div>
                    <h3>{title} ⭐ {rating}/5</h3>
                    <p style="margin:6px 0 0;">{review_text}</p>
                    <a class="read-more" href="{link}" target="_blank">Read More →</a>
                </div>
            """, unsafe_allow_html=True)

elif current == "Music Posts":
    st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
    if insta_df.empty:
        st.info("No music posts yet.")
    else:
        for _, r in insta_df.iterrows():
            caption = r.get("caption","")
            url = r.get("url","")
            st.markdown(f"""
                <div class="card">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div class="pill">🎵</div>
                        <div><h3 style="margin:0; font-size:1.4rem;">{caption}</h3></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            embed_html = f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:500px;"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
            """
            st.components.v1.html(embed_html, height=500, scrolling=True)

elif current == "About":
    st.markdown("<div class='section-title'>About Me</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box">
            <h2>Hi, I'm Harshita Kesarwani</h2>
            <p>A Delhi University student passionate about singing and movies. This blog is my space to share honest movie reviews, musical experiments, and slices from student life.</p>
            <p>I aim to connect with people who care about authenticity, storytelling, and creative expression.</p>
        </div>
    """, unsafe_allow_html=True)

elif current == "Contact":
    st.markdown("<div class='section-title'>Contact</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box">
            <p>📧 <strong>Email:</strong> <a href="mailto:harshita@example.com">harshita@example.com</a></p>
            <p>📸 <strong>Instagram:</strong> <a href="https://instagram.com/harshita.music" target="_blank">@harshita.music</a></p>
        </div>
    """, unsafe_allow_html=True)
