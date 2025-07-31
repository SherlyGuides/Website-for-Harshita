import streamlit as st
import pandas as pd
from urllib.parse import urlencode
from pathlib import Path
import base64

# -------- config --------
st.set_page_config(page_title="Harshita's Corner", layout="wide")

# -------- helpers --------
def img_to_base64(path: str):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

# -------- styling + carousel logic --------
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
    font-family: 'Inter', system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
}
body, .stApp { background: var(--bg); color: #1f1f28; }
.block-container { padding-top:80px; padding-left:2rem; padding-right:2rem; max-width:1140px; margin:auto; }
.site-header { text-align:center; margin-bottom:16px; padding:32px 20px; border-radius:14px; background: linear-gradient(135deg, rgba(159,122,234,0.1), #ffffff); position:relative; }
.site-header h1 { margin:0; font-size:2.8rem; font-weight:700; color: var(--purple-dark); }
.site-header p { margin:6px 0 0; font-size:1rem; color:#444; }

.tab-bar { display:flex; justify-content:center; gap:18px; flex-wrap:wrap; margin:24px 0 32px; }
.tab { padding:10px 18px; border-radius:999px; font-weight:600; font-size:14px; text-decoration:none; color:#4a4a63; background:#ece8f7; transition:all .15s; }
.tab:hover { background: rgba(159,122,234,0.12); }
.tab.active { background: var(--purple-dark); color:white; }

.card { background: var(--card); padding:18px 22px; border-radius: var(--radius); margin-bottom:22px; box-shadow: var(--shadow); border:1px solid rgba(159,122,234,0.1); }
.card h3 { margin:0 0 6px; font-size:1.5rem; color: var(--purple-dark); }
.meta { font-size:12px; color:#555; margin-bottom:6px; }
.read-more { display:inline-block; margin-top:6px; font-weight:600; color: var(--purple-dark); text-decoration:none; }
.section-title { font-size:1.8rem; font-weight:700; margin-bottom:14px; color: var(--purple-dark); }

.info-box { background:#ffffff; padding:22px 26px; border-radius: var(--radius); box-shadow:0 20px 40px -10px rgba(159,122,234,0.08); margin-bottom:30px; border:3px solid var(--purple); color:#1f1f28; }
.info-box h2 { margin-top:0; color: var(--purple-dark); }
.info-box p { margin:0.5rem 0; font-size:1rem; line-height:1.45; }
.info-box a { color: var(--purple-dark); font-weight:600; text-decoration:none; }

.pill { display:inline-block; background: var(--purple); color:white; padding:5px 14px; border-radius:999px; font-size:12px; font-weight:600; margin-right:8px; }

/* carousel */
.carousel-wrapper { position: relative; border-radius:16px; overflow:hidden; margin-bottom:24px; min-height:250px; }
.slide { position: absolute; inset:0; width:100%; height:100%; opacity:0; transition: opacity .8s ease-in-out; }
.slide.active { opacity:1; }
.slide-bg { width:100%; height:100%; background-size:cover; background-position:center; filter:brightness(0.95); }
.carousel-overlay { position:absolute; inset:0; background: rgba(255,255,255,0.55); backdrop-filter: blur(6px); display:flex; align-items:center; padding:30px 25px; gap:20px; flex-wrap:wrap; }
.carousel-overlay .text { flex:1; min-width:220px; }
.carousel-overlay h1 { margin:0; font-size:2.8rem; font-weight:700; color: var(--purple-dark); line-height:1.05; }
.carousel-overlay p { margin:6px 0 0; font-size:1rem; color:#444; }
.dot-container { position:absolute; bottom:12px; left:50%; transform:translateX(-50%); display:flex; gap:8px; z-index:5; }
.dot { width:10px; height:10px; border-radius:50%; background:rgba(255,255,255,0.6); cursor:pointer; border:2px solid var(--purple); transition: all .2s; }
.dot.active { background: var(--purple-dark); width:12px; height:12px; }
</style>
""", unsafe_allow_html=True)

# -------- load data --------
try:
    reviews_df = pd.read_csv("reviews.csv")
except Exception:
    reviews_df = pd.DataFrame(columns=["title", "review", "rating", "date", "read_time", "link"])

try:
    insta_df = pd.read_csv("instagram_links.csv")
except Exception:
    insta_df = pd.DataFrame(columns=["caption", "url"])

# -------- query params / tab logic --------
params = st.get_query_param()
current_tab = params.get("tab", ["Home"])[0]
if current_tab not in ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]:
    current_tab = "Home"

# -------- carousel header --------
# images must exist in root: header.jpeg, trail.jpeg, camera.jpeg
cover_images = ["header.jpeg", "trail.jpeg", "camera.jpeg"]
slides = []
for img in cover_images:
    b64 = img_to_base64(img)
    if b64:
        slides.append(b64)

if slides:
    # build HTML carousel
    slide_divs = ""
    for idx, b64 in enumerate(slides):
        active_cls = "active" if idx == 0 else ""
        slide_divs += f"""
        <div class="slide {active_cls}" data-index="{idx}">
          <div class="slide-bg" style="background-image:url('data:image/jpeg;base64,{b64}');"></div>
        </div>
        """
    header_block = f"""
    <div class="carousel-wrapper" id="carousel">
      {slide_divs}
      <div class="carousel-overlay">
        <div class="text">
          <h1>Harshita's Corner</h1>
          <p>Follow my journey as a DU student sharing movie reviews and music!</p>
        </div>
      </div>
      <div class="dot-container" id="dots"></div>
    </div>
    <script>
      const slides = document.querySelectorAll("#carousel .slide");
      const dotsContainer = document.getElementById("dots");
      let current = 0;
      const total = slides.length;
      function show(i){{
        slides.forEach((s,idx)=>{{ 
          if(idx===i) s.classList.add("active"); else s.classList.remove("active");
        }});
        Array.from(dotsContainer.children).forEach((d,idx)=> {{
          d.classList.toggle("active", idx===i);
        }});
      }}
      function build(){{
        for(let i=0;i<total;i++){{
          const d=document.createElement("div");
          d.className="dot"+(i===0?" active":"");
          d.onclick=()=>{{ current=i; show(current); }};
          dotsContainer.appendChild(d);
        }}
      }}
      function advance(){{
        current=(current+1)%total;
        show(current);
      }}
      build();
      setInterval(advance,5000);
    </script>
    """
    st.markdown(header_block, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="site-header">
        <h1>Harshita's Corner</h1>
        <p>Follow my journey as a DU student sharing movie reviews and music!</p>
    </div>
    """, unsafe_allow_html=True)

# -------- tab bar --------
def make_link(label):
    q = {"tab": label}
    href = "?" + urlencode(q)
    active_class = "active" if current_tab == label else ""
    return f"<a class='tab {active_class}' href='{href}'>{label}</a>"

tabs_html = "<div class='tab-bar'>" + "".join([make_link(l) for l in ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]]) + "</div>"
st.markdown(tabs_html, unsafe_allow_html=True)

# -------- content by tab --------
if current_tab == "Home":
    left, right = st.columns([2,1], gap="large")
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
                caption = r.get("caption", "")
                url = r.get("url", "")
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
            st.markdown(f"""
                <div class="card">
                    <div class="meta">{date} | {read_time} min read</div>
                    <h3>{title} ⭐ {rating}/5</h3>
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
            caption = r.get("caption", "")
            url = r.get("url", "")
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

elif current_tab == "About":
    st.markdown("<div class='section-title'>About Me</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box">
            <h2>Hi, I'm Harshita Kesarwani</h2>
            <p>A Delhi University student passionate about singing and movies. This blog is my space to share honest movie reviews, musical experiments, and slices from student life.</p>
            <p>I aim to connect with people who care about authenticity, storytelling, and creative expression.</p>
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
