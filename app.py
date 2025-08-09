import streamlit as st
import google.generativeai as genai

import first
import second
import third

st.set_page_config(page_title="Fresh Fetch", layout="wide")
st.title("Welcome to Fresh Fetch")

st.markdown("Choose your personal guide for today")

firstchoice, secondchoice, thirdchoice = st.columns(3)

if "selected_app" not in st.session_state:
  st.session_state.selected_app = "Individual Wellness Trainer"

with firstchoice:
  if st.button("Individual Wellness Trainer"):
    st.session_state.selected_app = "Individual Wellness Trainer"
with secondchoice:
  if st.button("360° Status Prep"):
    st.session_state.selected_app = "360° Status Prep"
with thirdchoice:
  if st.button("In-Depth Meal Planner"):
    st.session_state.selected_app = "Selective Meal Plan"


if st.session_state.selected_app == "Individual Wellness Trainer":
  first.run()
elif st.session_state.selected_app == "360° Status Prep":
  second.run()
elif st.session_state.selected_app == "Selective Meal Plan":
  third.run()

