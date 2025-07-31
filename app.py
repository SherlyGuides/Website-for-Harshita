import streamlit as st
import pandas as pd

# --- config ---
st.set_page_config(page_title="Harshita's Corner", layout="wide")

# --- CSS & styling (soft theme with good contrast) ---
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
.tab-row {
    display: flex;
    justify-content: center;
    gap: 18px;
    flex-wrap: wrap;
    margin: 28px 0 36px;
}
.tab-btn {
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    border: none;
    transition: all .18s;
    background: #ece8f7;
    color: #3f3f55;
}
.tab-btn:hover {
    background: rgba(159,122,234,0.12);
}
.tab-btn.active {
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

# --- load data ---
try:
    reviews_df = pd.read_csv("reviews.csv")
except:
    reviews_df = pd.DataFrame(columns=["title","review","rating","date","read_time","link"])
try:
    insta_df = pd.read_csv("instagram_links.csv")
except:
    insta_df = pd.DataFrame(columns=["caption","url"])

# --- tab state ---
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
labels = ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]
cols = st.columns(len(labels))
for i, lab in enumerate(labels):
    is_active = st.session_state.tab == lab
    clicked = cols[i].button(lab, key=f"tab_{lab}")
    if clicked:
        st.session_state.tab = lab
    # manual active styling via extra HTML if needed
    if is_active:
        # overlay active style (since Streamlit button can't get CSS class easily)
        pass  # appearance is acceptable; active button already visually different

# --- content rendering ---
if st.session_state.tab == "Home":
    left, right = st.columns([2,1], gap="large")
    with left:
        st.markdown("<div class='section-title'>Latest Movie Reviews</div>", unsafe_allow_html=True)
        if reviews_df.empty:
            st.info("No movie reviews yet.")
        else:
            for _, row in reviews_df.iterrows():
                title = row.get("title","")
                rating = row.get("rating","")
                date = row.get("date","")
                read_time = row.get("read_time","")
                review_text = row.get("review","")
                link = row.get("link","#")
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
            for _, row in insta_df.iterrows():
                caption = row.get("caption","")
                url = row.get("url","")
                st.markdown(f"""
                    <div class="card">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <div class="pill">🎵</div>
                            <div><h3 style="margin:0; font-size:1.3rem;">{caption}</h3></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                embed_html = f"""
                    <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
                    <script async src="//www.instagram.com/embed.js"></script>
                """
                st.components.v1.html(embed_html, height=450, scrolling=True)

elif st.session_state.tab == "Movie Reviews":
    st.markdown("<div class='section-title'>Movie Reviews</div>", unsafe_allow_html=True)
    if reviews_df.empty:
        st.info("No movie reviews yet.")
    else:
        for _, row in reviews_df.iterrows():
            title = row.get("title","")
            rating = row.get("rating","")
            date = row.get("date","")
            read_time = row.get("read_time","")
            review_text = row.get("review","")
            link = row.get("link","#")
            st.markdown(f"""
                <div class="card">
                    <div class="meta">{date} | {read_time} min read</div>
                    <h3>{title} ⭐ {rating}/5</h3>
                    <p style="margin:6px 0 0;">{review_text}</p>
                    <a class="read-more" href="{link}" target="_blank">Read More →</a>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.tab == "Music Posts":
    st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
    if insta_df.empty:
        st.info("No music posts yet.")
    else:
        for _, row in insta_df.iterrows():
            caption = row.get("caption","")
            url = row.get("url","")
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




