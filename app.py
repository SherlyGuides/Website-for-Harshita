import streamlit as st
import pandas as pd
import os
from urllib.parse import urlencode
from PIL import Image, ImageOps, ImageDraw
import io
import base64

st.set_page_config(page_title="Debug Harshita", layout="wide")

st.title("Debug: Harshita's Corner")

# --- show environment info ---
st.subheader("Tab / Query Param")
params = st.get_query_params()
current_tab = params.get("tab", ["Home"])[0]
if current_tab not in ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]:
    current_tab = "Home"
st.write("current_tab:", current_tab)

st.subheader("Files present")
for fname in ["trail.jpeg", "header.jpeg", "reviews.csv", "instagram_links.csv"]:
    st.write(f"{fname}: {'✅ exists' if os.path.exists(fname) else '❌ missing'}")

# --- try load images ---
st.subheader("Images preview")
def make_circular(img: Image.Image, size=(120, 120)):
    img = img.convert("RGBA")
    img = ImageOps.fit(img, size, centering=(0.5, 0.5))
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    img.putalpha(mask)
    return img

if os.path.exists("header.jpeg"):
    try:
        avatar = Image.open("header.jpeg")
        circ = make_circular(avatar)
        st.image(circ, caption="Avatar (circular)", width=120)
    except Exception as e:
        st.error(f"Failed loading header.jpeg: {e}")
else:
    st.info("header.jpeg not found.")

if os.path.exists("trail.jpeg"):
    try:
        banner = Image.open("trail.jpeg")
        st.image(banner, caption="Banner", use_column_width=True)
    except Exception as e:
        st.error(f"Failed loading trail.jpeg: {e}")
else:
    st.info("trail.jpeg not found.")

# --- load CSVs ---
st.subheader("CSV data")
try:
    reviews_df = pd.read_csv("reviews.csv")
    st.write("Reviews preview:", reviews_df.head())
except Exception as e:
    st.error(f"Error loading reviews.csv: {e}")
    reviews_df = pd.DataFrame()

try:
    insta_df = pd.read_csv("instagram_links.csv")
    st.write("Instagram links preview:", insta_df.head())
except Exception as e:
    st.error(f"Error loading instagram_links.csv: {e}")
    insta_df = pd.DataFrame()

# --- Simple tab navigation ---
st.subheader("Navigation")
tabs = ["Home", "Movie Reviews", "Music Posts", "About", "Contact"]
for t in tabs:
    href = "?" + urlencode({"tab": t})
    if t == current_tab:
        st.markdown(f"**{t}**", unsafe_allow_html=True)
    else:
        st.markdown(f"[{t}]({href})", unsafe_allow_html=True)

# --- Content stub ---
st.subheader(f"Content for: {current_tab}")
if current_tab == "Home":
    st.write("Would show latest movie reviews and music posts here.")
elif current_tab == "Movie Reviews":
    st.write("Movie Reviews section.")
elif current_tab == "Music Posts":
    st.write("Music Posts section.")
elif current_tab == "About":
    st.write("About Me section.")
elif current_tab == "Contact":
    st.write("Contact section.")

