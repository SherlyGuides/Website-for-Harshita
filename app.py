import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageDraw
import os
import io
import base64

# ---- page config ----
st.set_page_config(page_title="Harshita's Corner", layout="wide")

# ---- CSS + theme injection (must be top-level) ----
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --purple:#9f7aea;
  --purple-dark:#6e3cb0;
  --yellow-light:#fff9e6;
  --yellow-border:#ffe8b3;
  --bg:#fafaff;
  --card:#ffffff;
  --radius:14px;
  --shadow:0 20px 40px -10px rgba(159,122,234,0.15);
  font-family:'Inter', system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
}
body, .stApp { background: var(--bg) !important; color: #1f1f28 !important; }
h1, .section-title { color: var(--purple-dark) !important; margin:0; }
.block-container { padding-top:60px; max-width:1100px; margin:auto; }

/* nav tabs */
.tab-bar { display:flex; justify-content:center; gap:16px; flex-wrap:wrap; margin:14px 0 30px; }
.tab { padding:10px 20px; border-radius:999px; font-weight:600; font-size:14px; text-decoration:none; color:#4a4a63; background:#ece8f7; transition:all .2s; }
.tab:hover { background: rgba(159,122,234,0.12); }
.tab.active { background: var(--purple-dark); color:white; }

/* cards */
.section-title { font-size:1.7rem; font-weight:700; margin-bottom:12px; }
.card { background: var(--card); padding:18px 22px; border-radius: var(--radius); margin-bottom:22px; box-shadow: var(--shadow); border:1px solid rgba(159,122,234,0.1); }
.card h3 { margin:0 0 6px; font-size:1.5rem; }
.meta { font-size:12px; color:#555; margin-bottom:6px; }
.read-more { display:inline-block; margin-top:6px; font-weight:600; color: var(--purple-dark); text-decoration:none; }

/* info box */
.info-box { background:#fff; padding:22px 26px; border-radius: var(--radius); box-shadow:0 20px 40px -10px rgba(159,122,234,0.08); margin-bottom:30px; border:3px solid var(--purple); }
.pill { display:inline-block; background: var(--purple); color:white; padding:6px 16px; border-radius:999px; font-size:12px; font-weight:600; margin-right:8px; }
.callout { background: var(--yellow-light); border:1px solid var(--yellow-border); border-radius:12px; padding:14px 20px; margin-bottom:20px; display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
.callout .title { font-weight:700; font-size:1rem; }
.callout .desc { flex:1; }
.callout a { margin-left:auto; background: var(--purple-dark); color:white; padding:8px 16px; border-radius:999px; text-decoration:none; font-weight:600; font-size:0.85rem; }

.header-wrapper { position: relative; border-radius:16px; overflow:hidden; margin-bottom:32px; }
.header-bg { width:100%; height:260px; background-size:cover; background-position:center; filter:brightness(0.95); }
.header-overlay { position:absolute; inset:0; background:rgba(255,255,255,0.6); backdrop-filter:blur(6px); display:flex; align-items:center; padding:25px 30px; gap:24px; flex-wrap:wrap; }
.header-text { flex:1; min-width:220px; }
.header-text h1 { margin:0; font-size:2.8rem; font-weight:700; color: var(--purple-dark); line-height:1.05; }
.header-text p { margin:6px 0 0; font-size:1rem; color:#444; }
.avatar-container { flex-shrink:0; width:110px; height:110px; border-radius:999px; overflow:hidden; border:4px solid white; box-shadow:0 0 0 4px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# ---- helpers ----
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

# ---- load assets ----
# banner (background) and avatar
banner_url = None
avatar_b64 = None
if os.path.exists("trail.jpeg"):
    try:
        banner_url = "trail.jpeg"
    except:
        banner_url = None

if os.path.exists("header.jpeg"):
    try:
        raw = Image.open("header.jpeg")
        circ = make_circular(raw, size=(110,110))
        avatar_b64 = image_to_base64(circ)
    except:
        avatar_b64 = None

# ---- load data files (with safe fallback) ----
def load_reviews():
    if os.path.exists("reviews.csv"):
        try:
            df = pd.read_csv("reviews.csv")
            # Expect columns: title,rating,date,read_time,review,link
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def load_instagram():
    if os.path.exists("instagram_links.csv"):
        try:
            df = pd.read_csv("instagram_links.csv", header=None, names=["url"])
            # Normalize: expect full share/permalink like https://www.instagram.com/reel/XYZ/ or /p/...
            df["caption"] = "Latest Reel"
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

reviews_df = load_reviews()
insta_df = load_instagram()

# ---- determine active tab via query param fallback ----
if hasattr(st, "query_params"):
    params = st.query_params
else:
    params = st.experimental_get_query_params()
current_tab = params.get("tab", ["Home"])[0]
if current_tab not in ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]:
    current_tab = "Home"

# ---- header/banner section ----
header_html = "<div class='header-wrapper'>"
if banner_url:
    header_html += f"<div class='header-bg' style=\"background-image:url('{banner_url}');\"></div>"
else:
    header_html += "<div class='header-bg' style='background:linear-gradient(135deg,#f3ecff,#d9d7ff);'></div>"
header_html += "<div class='header-overlay'>"
if avatar_b64:
    header_html += f"<div class='avatar-container'><img src='data:image/png;base64,{avatar_b64}' style='width:100%;height:100%;object-fit:cover;'/></div>"
else:
    header_html += "<div class='avatar-container' style='background:var(--purple);'></div>"
header_html += """
  <div class='header-text'>
    <h1>Harshita's Corner</h1>
    <p>Follow my journey as a DU student sharing movie reviews and music!</p>
  </div>
"""
header_html += "</div></div>"

st.markdown(header_html, unsafe_allow_html=True)

# ---- callout + tabs ----
st.markdown(f"""
<div>
  <div class="callout">
    <div class="title">🔥 New Review Live!</div>
    <div class="desc">Check out the latest movie review and tell me what you think.</div>
    <a href="?tab=Movie Reviews">See Reviews</a>
  </div>
  <div class="tab-bar">
    {"".join(f"<a class='{'tab active' if current_tab==t else 'tab'}' href='?tab={t}'>{t}</a>" for t in ['Home','Movie Reviews','Music Posts','About','Contact'])}
  </div>
</div>
""", unsafe_allow_html=True)

# ---- content rendering ----
if current_tab == "Home":
    st.markdown("<div class='section-title'>Latest Movie Reviews</div>", unsafe_allow_html=True)
    if reviews_df.empty:
        st.info("No reviews.csv found or it's empty. Drop a CSV with columns: title,rating,date,read_time,review,link")
    else:
        for _, r in reviews_df.iterrows():
            title = r.get("title", "Untitled")
            rating = r.get("rating", "")
            date = r.get("date", "")
            read_time = r.get("read_time", "")
            review_text = r.get("review", "")
            link = r.get("link", "#")
            st.markdown(f"""
                <div class="card">
                  <div class="meta">{date} | {read_time} min read</div>
                  <h3>{title} ⭐ {rating}/5</h3>
                  <p>{review_text}</p>
                  <a class="read-more" href="{link}">Read More →</a>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
    if insta_df.empty:
        st.info("No instagram_links.csv found or it's empty. Put one URL per line (share/permalink).")
    else:
        for _, row in insta_df.iterrows():
            url = row["url"]
            caption = row.get("caption", "Music")
            st.markdown(f"""
                <div class="card">
                  <div style="display:flex; align-items:center; gap:10px;">
                    <div class="pill">🎵</div>
                    <div><h3 style="margin:0; font-size:1.2rem;">{caption}</h3></div>
                  </div>
                </div>
            """, unsafe_allow_html=True)
            # Instagram embed
            st.components.v1.html(f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
            """, height=420)

elif current_tab == "Movie Reviews":
    st.markdown("<div class='section-title'>All Movie Reviews</div>", unsafe_allow_html=True)
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
            st.markdown(f"""
                <div class="card">
                  <div class="meta">{date} | {read_time} min read</div>
                  <h3>{title} ⭐ {rating}/5</h3>
                  <p>{review_text}</p>
                  <a class="read-more" href="{link}">Read More →</a>
                </div>
            """, unsafe_allow_html=True)

elif current_tab == "Music Posts":
    st.markdown("<div class='section-title'>All Music Posts</div>", unsafe_allow_html=True)
    if insta_df.empty:
        st.warning("Nothing to show.")
    else:
        for _, row in insta_df.iterrows():
            url = row["url"]
            caption = row.get("caption", "Music Post")
            st.markdown(f"<div class='pill'>🎵 {caption}</div>", unsafe_allow_html=True)
            st.components.v1.html(f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
            """, height=420)

elif current_tab == "About":
    st.markdown("<div class='section-title'>About</div>", unsafe_allow_html=True)
    st.markdown("""
      <div class="info-box">
        <h2>Hi, I'm Harshita Kesarwani</h2>
        <p>Delhi University student sharing movie reviews and music. This space is where I reflect on films, share covers, and document the balance of college life and creativity.</p>
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

