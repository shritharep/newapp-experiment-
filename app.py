import streamlit as st
import google.generativeai as genai

import first
import second

st.set_page_config(page_title="FreshFetch", layout="wide")

st.markdown("Choose your personal guide for today")

firstchoice, secondchoice = st.columns(2)

if "selected_app" not in st.session_state:
  st.session_state.selected_app = "Individual Wellness Trainer"

with firstchoice:
  if st.button("Individual Wellness Trainer"):
    st.session_state.selected_app = "Individual Wellness Trainer"
with secondchoice:
  if st.button("360° Status Prep"):
    st.session_state.selected_app = "360° Status Prep"

if st.session_state.selected_app == "Individual Wellness Trainer":
  first.run()
elif st.session_state.selected_app == "360° Status Prep":
  second.run()
