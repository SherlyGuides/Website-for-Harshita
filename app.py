import streamlit as st
import pandas as pd
from urllib.parse import urlencode
from PIL import Image, ImageOps, ImageDraw
import base64
import io
import os

# ---- config ----
st.set_page_config(page_title="Harshita's Corner", layout="wide")

# ---- CSS injection (MUST be at top level, not inside any function) ----
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
  --radius:12px;
  --shadow:0 20px 40px -10px rgba(159,122,234,0.15);
  font-family:'Inter', system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
}
body, .stApp { background: var(--bg) !important; color: #1f1f28 !important; }
h1, .section-title { color: var(--purple-dark) !important; }
.block-container { padding-top:80px; max-width:1140px; margin:auto; }

/* tabs */
.tab-bar { display:flex; justify-content:center; gap:18px; flex-wrap:wrap; margin:16px 0 32px; }
.tab { padding:10px 18px; border-radius:999px; font-weight:600; font-size:14px; text-decoration:none; color:#4a4a63; background:#ece8f7; transition:all .15s; }
.tab:hover { background: rgba(159,122,234,0.12); }
.tab.active { background: var(--purple-dark); color:white; }

/* cards */
.section-title { font-size:1.8rem; font-weight:700; margin-bottom:14px; }
.card { background: var(--card); padding:18px 22px; border-radius: var(--radius); margin-bottom:22px; box-shadow: var(--shadow); border:1px solid rgba(159,122,234,0.1); }
.card h3 { margin:0 0 6px; font-size:1.5rem; }
.meta { font-size:12px; color:#555; margin-bottom:6px; }
.read-more { display:inline-block; margin-top:6px; font-weight:600; color: var(--purple-dark); text-decoration:none; }

.info-box { background:#fff; padding:22px 26px; border-radius: var(--radius); box-shadow:0 20px 40px -10px rgba(159,122,234,0.08); margin-bottom:30px; border:3px solid var(--purple); }
.pill { display:inline-block; background: var(--purple); color:white; padding:5px 14px; border-radius:999px; font-size:12px; font-weight:600; margin-right:8px; }
.callout { background: var(--yellow-light); border:1px solid var(--yellow-border); border-radius:10px; padding:12px 20px; margin-bottom:20px; display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
.callout .title { font-weight:700; }
.callout a { margin-left:auto; background: var(--purple-dark); color:white; padding:6px 14px; border-radius:999px; text-decoration:none; font-weight:600; font-size:0.85rem; }
</style>
""", unsafe_allow_html=True)

# ---- query params fallback ----
if hasattr(st, "query_params"):
    params = st.query_params
else:
    params = st.experimental_get_query_params()
current_tab = params.get("tab", ["Home"])[0]
if current_tab not in ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]:
    current_tab = "Home"

# ---- dummy data load (replace with your CSV later) ----
reviews_df = pd.DataFrame([
    {"title": "12th Fail", "rating": "5", "date": "2023-12-15", "read_time": "6", "review": "A movie about perseverance that resonated with me.", "link": "#"}
])
insta_df = pd.DataFrame([
    {"caption": "Latest Reel", "url": "https://www.instagram.com/p/Cs_example/"}
])

# ---- header ----
st.markdown(f"""
<div style="margin-top:20px;">
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

# ---- content ----
if current_tab == "Home":
    st.markdown("<div class='section-title'>Latest Movie Reviews</div>", unsafe_allow_html=True)
    for _, r in reviews_df.iterrows():
        st.markdown(f"""
            <div class="card">
              <div class="meta">{r['date']} | {r['read_time']} min read</div>
              <h3>{r['title']} ⭐ {r['rating']}/5</h3>
              <p>{r['review']}</p>
              <a class="read-more" href="{r['link']}">Read More →</a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Music Posts</div>", unsafe_allow_html=True)
    for _, r in insta_df.iterrows():
        st.markdown(f"""
            <div class="card">
              <div style="display:flex; align-items:center; gap:10px;">
                <div class="pill">🎵</div>
                <div><h3 style="margin:0; font-size:1.2rem;">{r['caption']}</h3></div>
              </div>
            </div>
        """, unsafe_allow_html=True)
        st.components.v1.html(f"""
            <blockquote class="instagram-media" data-instgrm-permalink="{r['url']}" data-instgrm-version="14" style="margin:auto; max-width:420px;"></blockquote>
            <script async src="//www.instagram.com/embed.js"></script>
        """, height=400)

elif current_tab == "About":
    st.markdown("<div class='section-title'>About</div>", unsafe_allow_html=True)
    st.markdown("""
      <div class="info-box">
        <h2>Hi, I'm Harshita Kesarwani</h2>
        <p>Delhi University student sharing movie reviews and music.</p>
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








