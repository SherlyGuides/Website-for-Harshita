import streamlit as st
import pandas as pd
import os
import time
import base64
from urllib.parse import urlencode
from PIL import Image
from io import BytesIO
import textwrap

# --- page config ---
st.set_page_config(page_title="Hey, it's Harshita Kesarwani", layout="wide")

# --- helpers ---
def safe_read_csv(path, cols):
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except Exception:
            return pd.DataFrame(columns=cols)
    return pd.DataFrame(columns=cols)

def image_to_data_url(path, max_size=None):
    if not os.path.exists(path):
        return None
    try:
        img = Image.open(path).convert("RGBA")
        if max_size:
            img.thumbnail(max_size, Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="PNG", quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{b64}"
    except Exception:
        return None

# --- carousel state & timing ---
if "carousel_idx" not in st.session_state:
    st.session_state.carousel_idx = 0
if "last_advance" not in st.session_state:
    st.session_state.last_advance = time.time()

CAROUSEL_INTERVAL = 3.0  # seconds
now = time.time()
carousel_files = [f for f in ["header.jpeg", "trail.jpeg", "camera.jpeg"] if os.path.exists(f)]
if carousel_files:
    if now - st.session_state.last_advance > CAROUSEL_INTERVAL:
        st.session_state.carousel_idx = (st.session_state.carousel_idx + 1) % len(carousel_files)
        st.session_state.last_advance = now
        # rerun to show next slide
        st.experimental_rerun()

# --- theme colors ---
PRIMARY = "#6e3cb0"      # dark purple
ACCENT = "#9f7aea"       # soft purple
BG = "#fafaff"
CARD = "#ffffff"
TEXT = "#1f1f28"

# --- custom CSS ---
st.markdown(
    f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --purple: {ACCENT};
  --purple-dark: {PRIMARY};
  --bg: {BG};
  --card: {CARD};
  --radius: 12px;
  --shadow: 0 20px 40px -10px rgba(159,122,234,0.15);
  font-family: 'Inter', system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
}}
body, .stApp {{
  background: var(--bg);
  color: {TEXT};
}}
.block-container {{
  max-width:1140px;
  padding-top:80px;
  padding-left:2rem;
  padding-right:2rem;
  margin:auto;
}}
.header-wrapper {{
  position: relative;
  border-radius:16px;
  overflow:hidden;
  margin-bottom:16px;
}}
.header-bg {{
  width:100%;
  height:260px;
  background-size:cover;
  background-position:center;
  filter:brightness(0.85);
  position:relative;
}}
.header-overlay {{
  position:absolute;
  inset:0;
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(6px);
  display:flex;
  align-items:center;
  gap:20px;
  padding:30px 25px;
  flex-wrap:wrap;
  min-height:160px;
  box-sizing:border-box;
}}
.header-text {{
  flex:1;
  min-width:220px;
}}
.header-text h1 {{
  margin:0;
  font-size:2.8rem;
  font-weight:700;
  color: var(--purple-dark);
  line-height:1.05;
}}
.header-text p {{
  margin:6px 0 0;
  font-size:1rem;
  color:#444;
}}
.avatar {{
  flex-shrink:0;
}}
.tab-bar {{
  display:flex;
  justify-content:center;
  gap:18px;
  flex-wrap:wrap;
  margin:24px 0 32px;
}}
.tab {{
  padding:10px 18px;
  border-radius:999px;
  font-weight:600;
  font-size:14px;
  text-decoration:none;
  color:#4a4a63;
  background:#ece8f7;
  transition: all .15s;
}}
.tab:hover {{
  background: rgba(159,122,234,0.12);
}}
.tab.active {{
  background: var(--purple-dark);
  color:white;
}}
.card {{
  background: var(--card);
  padding:18px 22px;
  border-radius: var(--radius);
  margin-bottom:22px;
  box-shadow: var(--shadow);
  border:1px solid rgba(159,122,234,0.1);
}}
.card h3 {{
  margin:0 0 6px;
  font-size:1.5rem;
  color: var(--purple-dark);
}}
.meta {{
  font-size:12px;
  color:#555;
  margin-bottom:6px;
}}
.read-more {{
  display:inline-block;
  margin-top:6px;
  font-weight:600;
  color: var(--purple-dark);
  text-decoration:none;
}}
.section-title {{
  font-size:1.8rem;
  font-weight:700;
  margin-bottom:14px;
  color: var(--purple-dark);
}}
.info-box {{
  background:#ffffff;
  padding:22px 26px;
  border-radius: var(--radius);
  box-shadow:0 20px 40px -10px rgba(159,122,234,0.08);
  margin-bottom:30px;
  border:3px solid var(--purple);
}}
.pill {{
  display:inline-block;
  background: var(--purple);
  color:white;
  padding:5px 14px;
  border-radius:999px;
  font-size:12px;
  font-weight:600;
  margin-right:8px;
}}
.callout {{
  background: rgba(255,245,235,0.9);
  border:1px solid rgba(255,200,150,0.6);
  border-radius:10px;
  padding:16px 24px;
  display:flex;
  gap:12px;
  align-items:center;
  flex-wrap:wrap;
  font-size:0.95rem;
  max-width:860px;
  margin:0 auto 32px;
}}
.callout .title {{
  font-weight:700;
}}
.callout .desc {{
  color:#4a4a63;
  flex:1;
}}
.callout a {{
  background: var(--purple-dark);
  color: white;
  padding:6px 14px;
  border-radius:999px;
  text-decoration:none;
  font-weight:600;
  font-size:0.85rem;
}}
</style>
""",
    unsafe_allow_html=True,
)

# --- load data ---
reviews_df = safe_read_csv("reviews.csv", ["title", "review", "rating", "date", "read_time", "link"])
insta_df = safe_read_csv("instagram_links.csv", ["caption", "url"])

# --- tab state ---
params = st.query_params
current_tab = params.get("tab", ["Home"])[0] if isinstance(params.get("tab", ["Home"]), list) else params.get("tab", "Home")
if current_tab not in ["Home", "Movie Reviews", "Music Posts", "Contact"]:
    current_tab = "Home"

# --- header / carousel ---
# background image from carousel
bg_url = None
if carousel_files:
    current_file = carousel_files[st.session_state.carousel_idx % len(carousel_files)]
    bg_url = image_to_data_url(current_file, max_size=(1400, 400))

# avatar selection with fallback
avatar_candidate = None
for candidate in ["camera.jpeg", "header.jpeg", "trail.jpeg"]:
    if os.path.exists(candidate):
        avatar_candidate = candidate
        break
avatar_url = image_to_data_url(avatar_candidate) if avatar_candidate else None

# header background style
header_bg_style = f"background: {BG};"
if bg_url:
    header_bg_style = f"background-image:url('{bg_url}');"

# avatar HTML
if avatar_url:
    avatar_html = textwrap.dedent(f"""\
        <div class="avatar">
            <div style="width:100px;height:100px;border-radius:50%;overflow:hidden;
                        border:3px solid white;box-shadow:0 8px 24px rgba(0,0,0,0.15);">
                <img src="{avatar_url}" style="width:100%;height:100%;object-fit:cover;" alt="avatar"/>
            </div>
        </div>""")
else:
    avatar_html = textwrap.dedent("""\
        <div class="avatar">
            <div style="width:100px;height:100px;border-radius:50%;display:flex;
                        align-items:center;justify-content:center;
                        background:rgba(159,122,234,0.1);font-weight:700;
                        color:var(--purple-dark);font-size:1.2rem;">
                HK
            </div>
        </div>""")

# render header/banner (without duplicate callout here)
st.markdown(
    f"""
<div class="header-wrapper">
  <div class="header-bg" style="{header_bg_style};">
    <div class="header-overlay">
      {avatar_html}
      <div class="header-text">
         <h1>Hey, it's Harshita Kesarwani</h1>
         <p>Follow my journey as a DU student sharing movie reviews and music!</p>
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- tabs ---
def make_link(label, current_tab):
    q = {"tab": label}
    href = "?" + urlencode(q)
    active_class = "active" if current_tab == label else ""
    return f"<a class='tab {active_class}' href='{href}'>{label}</a>"

tabs_html = "<div class='tab-bar'>" + "".join(
    make_link(l, current_tab) for l in ["Home", "Movie Reviews", "Music Posts", "Contact"]
) + "</div>"
st.markdown(tabs_html, unsafe_allow_html=True)

# --- moved callout below tabs ---
if current_tab in ["Movie Reviews"]:
    st.markdown(
        """
        <div class="callout">
          <div class="title">🔥 New Review Live!</div>
          <div class="desc">Check out the latest movie review and tell me what you think.</div>
          <a href="?tab=Movie%20Reviews">See Reviews →</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- content ---
if current_tab == "Home":
    left, right = st.columns([2, 1], gap="large")
    with left:
        st.markdown("<div class='section-title'>Latest Movie Reviews</div>", unsafe_allow_html=True)
        if reviews_df.empty:
            st.info("No movie reviews yet.")
        else:
            for _, r in reviews_df.iterrows():
                title = r.get("title", "")
                rating = r.get("rating", "")
                date = r.get("date", "")
                read_time = r.get("read_time", "")
                review_text = r.get("review", "")
                link = r.get("link", "#")
                st.markdown(
                    f"""
                    <div class="card">
                      <div class="meta">{date} | {read_time} min read</div>
                      <h3>{title} ⭐ {rating}/5</h3>
                      <p style="margin:6px 0 0;">{review_text}</p>
                      <a class="read-more" href="{link}" target="_blank">Read More →</a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    with right:
        st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
        if insta_df.empty:
            st.info("No music posts yet.")
        else:
            for _, r in insta_df.iterrows():
                caption = r.get("caption", "")
                url = r.get("url", "")
                st.markdown(
                    f"""
                    <div class="card">
                       <div style="display:flex; align-items:center; gap:10px;">
                          <div class="pill">🎵</div>
                          <div><h3 style="margin:0; font-size:1.25rem;">{caption}</h3></div>
                       </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                embed_html = f"""
                    <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
                """
                st.components.v1.html(embed_html, height=450, scrolling=True)
    # instagram embed script loaded once
    st.markdown(
        "<script async src=\"//www.instagram.com/embed.js\"></script>",
        unsafe_allow_html=True,
    )

elif current_tab == "Movie Reviews":
    st.markdown("<div class='section-title'>Movie Reviews</div>", unsafe_allow_html=True)
    if reviews_df.empty:
        st.info("No movie reviews yet.")
    else:
        for _, r in reviews_df.iterrows():
            title = r.get("title", "")
            rating = r.get("rating", "")
            date = r.get("date", "")
            read_time = r.get("read_time", "")
            review_text = r.get("review", "")
            link = r.get("link", "#")
            st.markdown(
                f"""
                <div class="card">
                  <div class="meta">{date} | {read_time} min read</div>
                  <h3>{title} ⭐ {rating}/5</h3>
                  <p style="margin:6px 0 0;">{review_text}</p>
                  <a class="read-more" href="{link}" target="_blank">Read More →</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

elif current_tab == "Music Posts":
    st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
    if insta_df.empty:
        st.info("No music posts yet.")
    else:
        for _, r in insta_df.iterrows():
            caption = r.get("caption", "")
            url = r.get("url", "")
            st.markdown(
                f"""
                <div class="card">
                   <div style="display:flex; align-items:center; gap:10px;">
                      <div class="pill">🎵</div>
                      <div><h3 style="margin:0; font-size:1.4rem;">{caption}</h3></div>
                   </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            embed_html = f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14" style="margin:auto; max-width:500px;"></blockquote>
            """
            st.components.v1.html(embed_html, height=500, scrolling=True)
    st.markdown(
        "<script async src=\"//www.instagram.com/embed.js\"></script>",
        unsafe_allow_html=True,
    )


elif current_tab == "Contact":
    st.markdown("<div class='section-title'>Contact</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-box">
          <p>📧 <strong>Email:</strong> <a href="mailto:harshitakesarwani@gmail.com">harshitakesarwani@gmail.com</a></p>
          <p>📸 <strong>Instagram:</strong> <a href="https://www.instagram.com/harshita.k_25/" target="_blank">@harshita.k_25</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
