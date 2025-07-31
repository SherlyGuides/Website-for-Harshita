import streamlit as st
import pandas as pd

# --- config ---
st.set_page_config(page_title="Harshita's Corner", layout="wide")

# --- CSS & styling ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --purple:#6a1b9a;
    --purple-dark:#4e2a8e;
    --bg:#ffffff;
    --card:#f9f9f9;
    --radius:14px;
    --shadow:0 25px 50px -12px rgba(106,27,154,0.15);
    font-family: 'Inter', system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
}
body, .stApp { background: var(--bg); color: #1f1f28; }
.block-container {
    padding-top: 80px;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1180px;
    margin: auto;
}
.site-header {
    text-align: center;
    margin-bottom: 10px;
    padding: 40px 25px;
    border-radius: 16px;
    background: linear-gradient(135deg, var(--purple-dark), var(--purple));
    color: white;
    position: relative;
}
.site-header h1 {
    margin: 0;
    font-size: 3rem;
    line-height: 1.05;
    font-weight: 700;
}
.site-header p {
    margin: 8px 0 0;
    font-size: 1rem;
    opacity: 0.95;
}
.tab-row {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
    margin: 30px 0 40px;
}
.tab-btn {
    padding: 10px 22px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    border: none;
    transition: all .2s;
    background: #f0f0f7;
    color: #3c3c4e;
}
.tab-btn:hover {
    background: rgba(106,27,154,0.07);
}
.tab-btn.active {
    background: var(--purple);
    color: white;
    box-shadow: 0 14px 40px -5px rgba(106,27,154,0.4);
}
.card {
    background: var(--card);
    padding: 22px 24px;
    border-radius: var(--radius);
    margin-bottom: 24px;
    box-shadow: var(--shadow);
    border: 1px solid rgba(106,27,154,0.08);
}
.card h3 {
    margin: 0 0 6px;
    font-size: 1.55rem;
    color: var(--purple-dark);
}
.meta {
    font-size: 12px;
    color: #555;
    margin-bottom: 6px;
}
.read-more {
    display: inline-block;
    margin-top: 8px;
    font-weight: 600;
    color: var(--purple);
    text-decoration: none;
}
.section-title {
    font-size: 1.9rem;
    font-weight: 700;
    margin-bottom: 18px;
    color: var(--purple-dark);
}
.info-box {
    background: #ffffff;
    padding: 24px 28px;
    border-radius: var(--radius);
    box-shadow: 0 20px 40px -10px rgba(106,27,154,0.08);
    margin-bottom: 30px;
    border: 4px solid var(--purple);
    color: #1f1f28;
}
.info-box h2 {
    margin-top: 0;
    color: var(--purple-dark);
}
.info-box p {
    margin: 0.5rem 0;
    font-size: 1rem;
    line-height: 1.5;
}
.info-box a {
    color: var(--purple);
    font-weight: 600;
    text-decoration: none;
}
.pill {
    display: inline-block;
    background: var(--purple);
    color: white;
    padding: 6px 14px;
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
    reviews_df = pd.DataFrame(columns=["title", "review", "rating", "date", "read_time", "link"])
try:
    insta_df = pd.read_csv("instagram_links.csv")
except:
    insta_df = pd.DataFrame(columns=["caption", "url"])

# --- state ---
if "tab" not in st.session_state:
    st.session_state.tab = "Home"

# --- header ---
st.markdown("""
    <div class="site-header">
        <h1>Harshita's Corner</h1>
        <p>Follow my journey as a DU student sharing movie reviews and music!</p>
    </div>
""", unsafe_allow_html=True)

# --- tabs ---
tab_labels = ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]
tab_cols = st.columns(len(tab_labels))
for i, label in enumerate(tab_labels):
    is_active = st.session_state.tab == label
    btn = tab_cols[i].button(label, key=f"tab_{label}")
    if btn:
        st.session_state.tab = label

# --- content ---
if st.session_state.tab == "Home":
    left, right = st.columns([2, 1], gap="large")
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
                        <p style='margin:6px 0 0;'>{review_text}</p>
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
                st.markdown(f"""
                    <div class='card'>
                        <div style="display:flex; align-items:center; gap:10px;">
                            <div class="pill">🎵</div>
                            <div>
                                <h3 style="margin:0; font-size:1.3rem;">{caption}</h3>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                embed_html = f"""
                    <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
                    <script async src="//www.instagram.com/embed.js"></script>
                """
                st.components.v1.html(embed_html, height=480, scrolling=True)

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
                    <p style='margin:6px 0 0;'>{review_text}</p>
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
            st.markdown(f"""
                <div class='card'>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div class="pill">🎵</div>
                        <div>
                            <h3 style="margin:0; font-size:1.4rem;">{caption}</h3>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            embed_html = f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:500px;"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
            """
            st.components.v1.html(embed_html, height=500, scrolling=True)

elif st.session_state.tab == "About":
    st.markdown("<div class='section-title'>About Me</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box">
            <h2>Hi, I'm Harshita Kesarwani</h2>
            <p>A Delhi University student passionate about singing and movies. This blog is my space to share honest movie reviews, musical experiments, and slices from student life.</p>
            <p>I aim to connect with people who care about authenticity, storytelling, and creative expression.</p>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.tab == "Contact":
    st.markdown("<div class='section-title'>Contact</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box">
            <p>📧 <strong>Email:</strong> <a href="mailto:harshita@example.com">harshita@example.com</a></p>
            <p>📸 <strong>Instagram:</strong> <a href="https://instagram.com/harshita.music" target="_blank">@harshita.music</a></p>
        </div>
    """, unsafe_allow_html=True)


