import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageDraw
import os
import io
import base64

st.set_page_config(page_title="Harshita's Corner", layout="wide")

# --- helpers ---
def make_circular(img: Image.Image, size=(110, 110)) -> Image.Image:
    img = img.convert("RGBA")
    img = ImageOps.fit(img, size, centering=(0.5, 0.5))
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    img.putalpha(mask)
    return img

def image_to_base64(img: Image.Image, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt, quality=85)
    return base64.b64encode(buf.getvalue()).decode()

# --- load assets ---
banner_path = "trail.jpeg" if os.path.exists("trail.jpeg") else None
avatar_b64 = None
if os.path.exists("header.jpeg"):
    try:
        raw = Image.open("header.jpeg")
        circ = make_circular(raw, size=(110, 110))
        avatar_b64 = image_to_base64(circ)
    except:
        avatar_b64 = None

# --- load data ---
def load_reviews():
    if os.path.exists("reviews.csv"):
        try:
            df = pd.read_csv("reviews.csv")
            return df
        except Exception as e:
            st.warning(f"Could not read reviews.csv: {e}")
    return pd.DataFrame()

def load_instagram():
    if os.path.exists("instagram_links.csv"):
        try:
            df = pd.read_csv("instagram_links.csv", header=None, names=["url"])
            df["caption"] = "Music Reel"
            return df
        except Exception as e:
            st.warning(f"Could not read instagram_links.csv: {e}")
    return pd.DataFrame()

reviews_df = load_reviews()
insta_df = load_instagram()

# --- theme colors (used inline) ---
PRIMARY = "#6e3cb0"  # purple dark
ACCENT = "#9f7aea"
BG = "#fafaff"
CARD_BG = "#ffffff"

# --- header/banner ---
with st.container():
    cols = st.columns([1, 3, 2])
    with cols[0]:
        if avatar_b64:
            st.image(f"data:image/png;base64,{avatar_b64}", width=110)
        else:
            st.write("")  # placeholder
    with cols[1]:
        st.markdown(f"<h1 style='color:{PRIMARY};margin-bottom:4px;'>Harshita's Corner</h1>", unsafe_allow_html=True)
        st.markdown("<p style='margin:0;'>Follow my journey as a DU student sharing movie reviews and music!</p>", unsafe_allow_html=True)
    with cols[2]:
        # optional small callout
        st.markdown(f"<div style='background:#fff3e6;border:1px solid #ffe8b3;border-radius:8px;padding:10px;'>"
                    f"<strong style='color:#d35400;'>🔥 New Review Live!</strong><br>"
                    f"<small>Check out the latest movie review and tell me what you think.</small><br>"
                    f"<a href='?tab=Movie Reviews'>See Reviews</a></div>", unsafe_allow_html=True)

# banner image
if banner_path:
    st.image(banner_path, use_column_width=True, caption=None)

st.divider()

# --- navigation (tabs) ---
tab = st.radio("", ["Home", "Movie Reviews", "Music Posts", "About", "Contact"], index=0, horizontal=True)

# --- content ---
if tab == "Home":
    st.subheader("Latest Movie Reviews")
    if reviews_df.empty:
        st.info("No reviews available. Place a `reviews.csv` with columns: title,rating,date,read_time,review,link")
    else:
        for _, r in reviews_df.iterrows():
            title = r.get("title", "Untitled")
            rating = r.get("rating", "")
            date = r.get("date", "")
            read_time = r.get("read_time", "")
            review_text = r.get("review", "")
            link = r.get("link", "#")
            st.markdown(
                f"""
                <div style="background:{CARD_BG};padding:16px;border-radius:12px;box-shadow:0 8px 20px rgba(0,0,0,0.04);margin-bottom:16px;">
                  <div style="font-size:12px;color:#555;margin-bottom:4px;">{date} | {read_time} min read</div>
                  <h2 style="margin:0;color:{PRIMARY};">{title} ⭐ {rating}/5</h2>
                  <p style="margin:8px 0 0;">{review_text}</p>
                  <a href="{link}" style="color:{ACCENT};font-weight:600;text-decoration:none;">Read More →</a>
                </div>
                """, unsafe_allow_html=True
            )

    st.subheader("Music Posts")
    if insta_df.empty:
        st.info("No Instagram links. Provide `instagram_links.csv` with one share/permalink per line.")
    else:
        for _, row in insta_df.iterrows():
            url = row["url"]
            caption = row.get("caption", "Music Reel")
            st.markdown(f"**🎵 {caption}**")
            st.components.v1.html(f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
            """, height=420)

elif tab == "Movie Reviews":
    st.subheader("All Movie Reviews")
    if reviews_df.empty:
        st.warning("No reviews to show.")
    else:
        for _, r in reviews_df.iterrows():
            title = r.get("title", "Untitled")
            rating = r.get("rating", "")
            date = r.get("date", "")
            read_time = r.get("read_time", "")
            review_text = r.get("review", "")
            link = r.get("link", "#")
            st.markdown(
                f"""
                <div style="background:{CARD_BG};padding:16px;border-radius:12px;box-shadow:0 8px 20px rgba(0,0,0,0.04);margin-bottom:16px;">
                  <div style="font-size:12px;color:#555;margin-bottom:4px;">{date} | {read_time} min read</div>
                  <h2 style="margin:0;color:{PRIMARY};">{title} ⭐ {rating}/5</h2>
                  <p style="margin:8px 0 0;">{review_text}</p>
                  <a href="{link}" style="color:{ACCENT};font-weight:600;text-decoration:none;">Read More →</a>
                </div>
                """, unsafe_allow_html=True
            )

elif tab == "Music Posts":
    st.subheader("All Music Posts")
    if insta_df.empty:
        st.warning("No music posts to show.")
    else:
        for _, row in insta_df.iterrows():
            url = row["url"]
            caption = row.get("caption", "Music Reel")
            st.markdown(f"**🎵 {caption}**")
            st.components.v1.html(f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
            """, height=420)

elif tab == "About":
    st.subheader("About")
    st.markdown(
        """
        <div style="background:#fff;padding:18px;border-radius:10px;box-shadow:0 12px 30px rgba(0,0,0,0.04);">
            <h2 style="color:#5e2ca5;margin-top:0;">Hi, I'm Harshita Kesarwani</h2>
            <p>Delhi University student sharing movie reviews and music. This space is where I reflect on films, share covers, and document the balance of college life and creativity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif tab == "Contact":
    st.subheader("Contact")
    st.markdown(
        """
        <div style="background:#fff;padding:18px;border-radius:10px;box-shadow:0 12px 30px rgba(0,0,0,0.04);">
            <p>📧 <strong>Email:</strong> <a href="mailto:harshita@example.com">harshita@example.com</a></p>
            <p>📸 <strong>Instagram:</strong> <a href="https://instagram.com/harshita.music" target="_blank">@harshita.music</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


