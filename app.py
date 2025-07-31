import streamlit as st
import pandas as pd
from urllib.parse import urlencode
from PIL import Image, ImageOps, ImageDraw
import os
import io
import base64

# --- config ---
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
avatar_b64 = None
if os.path.exists("header.jpeg"):
    try:
        raw = Image.open("header.jpeg")
        circ = make_circular(raw, size=(110, 110))
        avatar_b64 = image_to_base64(circ)
    except Exception:
        avatar_b64 = None

banner_path = "trail.jpeg" if os.path.exists("trail.jpeg") else None

# --- load data ---
def load_reviews():
    if os.path.exists("reviews.csv"):
        try:
            df = pd.read_csv("reviews.csv")
            return df
        except Exception as e:
            st.warning(f"Could not read reviews.csv: {e}")
    return pd.DataFrame(columns=["title", "rating", "date", "read_time", "review", "link"])

def load_instagram():
    if os.path.exists("instagram_links.csv"):
        try:
            df = pd.read_csv("instagram_links.csv", header=None, names=["url"])
            df["caption"] = "Music Reel"
            return df
        except Exception as e:
            st.warning(f"Could not read instagram_links.csv: {e}")
    return pd.DataFrame(columns=["url", "caption"])

reviews_df = load_reviews()
insta_df = load_instagram()

# --- styling (minimal custom theme) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --purple:#9f7aea;
  --purple-dark:#6e3cb0;
  --bg:#fafaff;
  --card:#ffffff;
  --radius:12px;
  --shadow:0 20px 40px -10px rgba(159,122,234,0.15);
  font-family:'Inter',system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
}
body, .stApp { background: var(--bg); }
h1, h2, h3 { font-family:'Inter',sans-serif; }
.section-title { font-size:1.8rem; font-weight:700; margin-bottom:12px; color: var(--purple-dark); }
.card { background: var(--card); padding:16px 20px; border-radius:var(--radius); box-shadow: var(--shadow); margin-bottom:18px; border:1px solid rgba(159,122,234,0.1); }
.meta { font-size:12px; color:#555; margin-bottom:6px; }
.read-more { color: var(--purple); font-weight:600; text-decoration:none; }
.tab { padding:8px 16px; border-radius:999px; font-weight:600; font-size:14px; text-decoration:none; margin:0 6px; display:inline-block; }
.tab-inactive { background:#ece8f7; color:#4a4a63; }
.tab-active { background: var(--purple-dark); color:#fff; }
.pill { background: var(--purple); color:#fff; padding:5px 12px; border-radius:999px; font-size:12px; font-weight:600; display:inline-block; margin-right:8px; }
.info-box { background:#fff; padding:20px; border-radius:12px; box-shadow:0 16px 35px rgba(0,0,0,0.03); border:3px solid var(--purple); }
.header { padding:30px 25px; border-radius:14px; background: linear-gradient(135deg, rgba(159,122,234,0.08), #ffffff); margin-bottom:24px; display:flex; gap:20px; align-items:center; flex-wrap:wrap; }
.header-title { margin:0; font-size:2.8rem; font-weight:700; color: var(--purple-dark); }
.header-sub { margin:4px 0 0; color:#444; }
</style>
""", unsafe_allow_html=True)

# --- determine current tab ---
current_tab = st.query_params.get("tab", ["Home"])[0]
if current_tab not in ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]:
    current_tab = "Home"

# --- header/banner layout ---
st.markdown("<div class='header'>", unsafe_allow_html=True)
left_col, mid_col, right_col = st.columns([1, 3, 2])
with left_col:
    if avatar_b64:
        st.image(f"data:image/png;base64,{avatar_b64}", width=110)
with mid_col:
    st.markdown("<div>", unsafe_allow_html=True)
    st.markdown("<div class='header-title'>Harshita's Corner</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-sub'>Follow my journey as a DU student sharing movie reviews and music!</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with right_col:
    st.markdown(f"""
        <div style="background:#fff7f0;border:1px solid #ffe2d0;border-radius:10px;padding:10px;">
            <div style="font-weight:600;color:#d35400;">🔥 New Review Live!</div>
            <div style="font-size:0.9rem;">Check out the latest movie review and tell me what you think.</div>
            <div style="margin-top:4px;"><a href="?tab=Movie+Reviews" style="text-decoration:none;color: #6e3cb0;font-weight:600;">See Reviews →</a></div>
        </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if banner_path:
    st.image(banner_path, use_column_width=True)

# --- tab bar ---
tab_labels = ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]
tabs_html = "<div style='text-align:center; margin-top:16px;'>"
for label in tab_labels:
    safe_label = label.replace(" ", "+")
    active = "tab-active" if current_tab == label else "tab-inactive"
    href = "?" + urlencode({"tab": label})
    tabs_html += f"<a class='tab {active}' href='{href}'>{label}</a>"
tabs_html += "</div>"
st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<hr style='margin:24px 0 32px;'>", unsafe_allow_html=True)

# --- content ---
if current_tab == "Home":
    left, right = st.columns([2,1], gap="large")
    with left:
        st.markdown("<div class='section-title'>Latest Movie Reviews</div>", unsafe_allow_html=True)
        if reviews_df.empty:
            st.info("No movie reviews yet. Populate reviews.csv with columns: title,rating,date,read_time,review,link")
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
                        <h3 style="margin:4px 0 6px;">{title} ⭐ {rating}/5</h3>
                        <p style="margin:6px 0 0;">{review_text}</p>
                        <a class="read-more" href="{link}" target="_blank">Read More →</a>
                    </div>
                """, unsafe_allow_html=True)
    with right:
        st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
        if insta_df.empty:
            st.info("No Instagram posts. Provide instagram_links.csv with one full share/permalink URL per line.")
        else:
            for _, row in insta_df.iterrows():
                url = row["url"]
                st.markdown(f"""
                    <div class="card">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <div class="pill">🎵</div>
                            <div><div style="font-size:1.2rem;font-weight:600;margin:0;">Latest Reel</div></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.components.v1.html(f"""
                    <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
                    <script async src="//www.instagram.com/embed.js"></script>
                """, height=450, scrolling=False)

elif current_tab == "Movie Reviews":
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
                    <h3 style="margin:4px 0 6px;">{title} ⭐ {rating}/5</h3>
                    <p style="margin:6px 0 0;">{review_text}</p>
                    <a class="read-more" href="{link}" target="_blank">Read More →</a>
                </div>
            """, unsafe_allow_html=True)

elif current_tab == "Music Posts":
    st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
    if insta_df.empty:
        st.info("No music posts yet.")
    else:
        for _, r in insta_df.iterrows():
            url = r["url"]
            st.markdown(f"""
                <div class="card">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div class="pill">🎵</div>
                        <div><div style="font-size:1.4rem;font-weight:600;margin:0;">Music Reel</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.components.v1.html(f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:500px;"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
            """, height=500, scrolling=False)

elif current_tab == "About":
    st.markdown("<div class='section-title'>About</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box">
            <h2>Hi, I'm Harshita Kesarwani</h2>
            <p>Delhi University student sharing movie reviews and music. This blog is my space to reflect, create, and connect through storytelling and song.</p>
        </div>
    """, unsafe_allow_html=True)

elif current_tab == "Contact":
    st.markdown("<div class='section-title'>Contact</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box">
            <p>📧 <strong>Email:</strong> <a href="mailto:harshita@example.com">harshita@example.com</a></p>
            <p>📸 <strong>Instagram:</strong> <a href="https://instagram.com/harshita.music" target="_blank">@harshita.music</a></p>
        </div>
    """, unsafe_allow_html=True)

