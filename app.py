import streamlit as st
st.set_page_config(page_title="CSS Test", layout="wide")

css = """
<style>
  body { background: #fafaff; font-family: system-ui, -apple-system; }
  h1 { color: #9f7aea; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)
st.title("If this title is purple and background light, CSS injection is working")


