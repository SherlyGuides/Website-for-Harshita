import streamlit as st
import pandas as pd
import os
import time
from urllib.parse import urlencode

# --- page config ---
st.set_page_config(page_title="Harshita's Corner", layout="wide")

# --- helper to load CSVs safely ---
def load_csv(path, cols):
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except Exception:
            return pd.DataFrame(columns=cols)
    else:
        return pd.DataFrame(columns=cols)

reviews_df = load_csv("reviews.csv", ["title", "review", "rating", "date", "read_time", "link"])
insta_df = load_csv("instagram_links.csv", ["caption", "url"])

# --- carousel state ---
if "carousel_idx" not in st.session_state:
    st.session_state.carousel_idx = 0
# Advance every time this runs if enough time has passed
if "last_advance" not in st.session_state:
    st.session_state.last_advance = time.time()

# Rotate every 3 seconds
if time.time() - st.session_state.last_advance > 3:
    st.session_state.carousel_idx = (st.session_state.carousel_idx + 1) % 3
    st.session_state.last_advance = time.time()
    st.experimental_rerun()

# --- images for carousel ---
carousel_images = []
for fname in ["header.jpeg", "trail.jpeg", "camera.jpeg"]:
    if os.path.exists(fname):
        carousel_images.append(fname)
# Fallback if none exist
if not carousel_images:
    carousel_images = []

# --- theme colors (soft purple/light) ---
PRIMARY = "#6e3cb0"  # purple dark
ACCENT = "#9f7aea"  # light purple
BG = "#fafaff"
CARD_BG = "#ffffff"
TEXT = "#1f1f28"

# --- header / carousel ---
st.markdown(
    f"""
    <div style="
        position: relative;
        border-radius:16px;
        overflow:hidden;
        margin: 0 auto 24px;
        max-width:1140px;
        background: {CARD_BG};
        box-shadow: 0 20px 40px -10px rgba(159,122,234,0.1);
    ">
        <!-- carousel -->
        <div style="position:relative; min-height:240px; display:flex; align-items:center; justify-content:center; background:#f0f0fa; overflow:hidden;">
    """,
    unsafe_allow_html=True,
)

# Show current carousel image
if carousel_images:
    current = carousel_images[st.session_state.carousel_idx % len(carousel_images)]
    st.image(current, use_column_width=True, caption=None)
else:
    st.markdown(
        f"""
        <div style="padding:60px; text-align:center;">
            <h2 style="margin:0;color:{PRIMARY};">Harshita's Corner</h2>
            <p style="margin:4px 0 0;color:{TEXT};">Follow my journey as a DU student sharing movie reviews and music!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Overlay title (absolute)
st.markdown(
    f"""
    <div style="position: relative; max-width:1140px; margin: -160px auto 40px; padding:20px 30px; display:flex; gap:20px; align-items:center; flex-wrap:wrap;">
        <div style="flex-shrink:0;">
            <div style="width:100px; height:100px; border-radius:50%; overflow:hidden; border:3px solid white; box-shadow:0 8px 24px rgba(0,0,0,0.15);">
                <img src="trail.jpeg" style="width:100%;height:100%;object-fit:cover;" alt="avatar"/>
            </div>
        </div>
        <div style="flex:1; min-width:220px;">
            <h1 style="margin:0;font-size:2.4rem;color:{PRIMARY};">Harshita's Corner</h1>
            <p style="margin:4px 0 0;color:#444;">Follow my journey as a DU student sharing movie reviews and music!</p>
        </div>
        <div style="margin-left:auto; min-width:200px;">
            <div style="background:#fff4ec; padding:12px 16px; border-radius:10px; border:1px solid rgba(159,122,234,0.3);">
                <div style="font-weight:600;margin:0;color:{PRIMARY};">🔥 New Review Live!</div>
                <div style="font-size:0.9rem; margin:4px 0;">Check out the latest movie review and tell me what you think.</div>
                <div><a href="#movie-reviews" style="text-decoration:none; font-weight:600; color:{ACCENT};">See Reviews →</a></div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- tabs (using native) ---
tab_labels = ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]
tabs = st.tabs(tab_labels)

# Utility for card rendering
def render_review_card(r):
    title = r.get("title", "")
    rating = r.get("rating", "")
    date = r.get("date", "")
    read_time = r.get("read_time", "")
    review_text = r.get("review", "")
    link = r.get("link", "#")
    st.markdown(
        f"""
        <div style="background:{CARD_BG}; padding:18px 22px; border-radius:14px; margin-bottom:22px; box-shadow:0 20px 40px -10px rgba(159,122,234,0.08); border:1px solid rgba(159,122,234,0.1);">
            <div style="font-size:12px;color:#555;margin-bottom:6px;">{date} | {read_time} min read</div>
            <h3 style="margin:0 0 6px;color:{PRIMARY}; font-size:1.5rem;">{title} ⭐ {rating}/5</h3>
            <p style="margin:6px 0 0;color:{TEXT};">{review_text}</p>
            <a href="{link}" target="_blank" style="display:inline-block;margin-top:8px;font-weight:600;color:{ACCENT}; text-decoration:none;">Read More →</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_insta_card(caption, url):
    st.markdown(
        f"""
        <div style="background:{CARD_BG}; padding:16px 18px; border-radius:14px; margin-bottom:22px; box-shadow:0 20px 40px -10px rgba(159,122,234,0.06); border:1px solid rgba(159,122,234,0.08);">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                <div style="background:{PRIMARY}; color:white; padding:6px 12px; border-radius:999px; font-size:12px; font-weight:600;">🎵 Music</div>
                <div><h3 style="margin:0;font-size:1.25rem;color:{PRIMARY};">{caption}</h3></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    embed_html = f"""
        <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:500px;"></blockquote>
        <script async src="//www.instagram.com/embed.js"></script>
    """
    st.components.v1.html(embed_html, height=500, scrolling=True)

# --- Home tab ---
with tabs[0]:
    col1, col2 = st.columns([2, 1], gap="large")
    with col1:
        st.markdown(f"<div style='font-size:1.8rem;font-weight:700;color:{PRIMARY};margin-bottom:12px;'>Latest Movie Reviews</div>", unsafe_allow_html=True)
        if reviews_df.empty:
            st.info("No movie reviews yet.")
        else:
            for _, r in reviews_df.iterrows():
                render_review_card(r)
    with col2:
        st.markdown(f"<div style='font-size:1.8rem;font-weight:700;color:{PRIMARY};margin-bottom:12px;'>Music Posts</div>", unsafe_allow_html=True)
        if insta_df.empty:
            st.info("No music posts yet.")
        else:
            for _, r in insta_df.iterrows():
                caption = r.get("caption", "")
                url = r.get("url", "")
                render_insta_card(caption, url)

# --- Movie Reviews tab ---
with tabs[1]:
    st.markdown(f"<div id='movie-reviews' style='font-size:1.8rem;font-weight:700;color:{PRIMARY};margin-bottom:12px;'>Movie Reviews</div>", unsafe_allow_html=True)
    if reviews_df.empty:
        st.info("No movie reviews yet.")
    else:
        for _, r in reviews_df.iterrows():
            render_review_card(r)

# --- Music Posts tab ---
with tabs[2]:
    st.markdown(f"<div style='font-size:1.8rem;font-weight:700;color:{PRIMARY};margin-bottom:12px;'>Music Posts</div>", unsafe_allow_html=True)
    if insta_df.empty:
        st.info("No music posts yet.")
    else:
        for _, r in insta_df.iterrows():
            caption = r.get("caption", "")
            url = r.get("url", "")
            render_insta_card(caption, url)

# --- About tab ---
with tabs[3]:
    st.markdown(f"<div style='font-size:1.8rem;font-weight:700;color:{PRIMARY};margin-bottom:12px;'>About Me</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background:{CARD_BG}; padding:22px 26px; border-radius:14px; box-shadow:0 20px 40px -10px rgba(159,122,234,0.08); border:1px solid rgba(159,122,234,0.1); max-width:900px;">
            <h2 style="margin-top:0;color:{PRIMARY};">Hi, I'm Harshita Kesarwani</h2>
            <p style="margin:4px 0;color:{TEXT};">A Delhi University student passionate about singing and movies. This blog is my space to share honest movie reviews, musical experiments, and slices from student life.</p>
            <p style="margin:4px 0;color:{TEXT};">I aim to connect with people who care about authenticity, storytelling, and creative expression.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Contact tab ---
with tabs[4]:
    st.markdown(f"<div style='font-size:1.8rem;font-weight:700;color:{PRIMARY};margin-bottom:12px;'>Contact</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background:{CARD_BG}; padding:22px 26px; border-radius:14px; box-shadow:0 20px 40px -10px rgba(159,122,234,0.08); border:1px solid rgba(159,122,234,0.1); max-width:700px;">
            <p style="margin:6px 0;"><strong>📧 Email:</strong> <a href="mailto:harshita@example.com">harshita@example.com</a></p>
            <p style="margin:6px 0;"><strong>📸 Instagram:</strong> <a href="https://instagram.com/harshita.music" target="_blank">@harshita.music</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


