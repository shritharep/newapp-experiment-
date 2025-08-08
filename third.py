import streamlit as st
import google.generativeai as genai

#page 1
st.text("Welcome to....")
st.markdown("<h1 style='text-align: center; color: black;'>Fresh Fetch</h1>", unsafe_allow_html=True)


#defined the variables
contraints={}
dietary_options=["Vegan", "Vegetarian", "Non-Vegetarian", "Pescatarian", "Omnivore"]
meal_preptime=["All Day", "Breakfast","Brunch", "Lunch", "Dinner"]


# Ask for user input
name = st.text_input("Enter your name")
dietary_restrictions = st.selectbox("What are your dietary restrictions?",dietary_options)
meal_time = st.selectbox("What is your meal time?",meal_preptime)
kitchen_restrictions = st.text_input("What are your kitchen restrictions? ex. materials you lack")
goal = st.text_input("Enter your goal or purpose for this meal")
caloric_max=st.number_input("How many calories is the maximum amount of calories you want your meal to have? :")

#button to switch pages (to page 1)
if st.button("Submit", use_container_width=True):
    st.session_state["meal_time"]= meal_time
    st.session_state["dietary_restriction"]= dietary_restrictions
    st.session_state["kitchen_restrictions"]= kitchen_restrictions
    st.session_state["caloric_max"]= caloric_max
    st.session_state["name"]= name
    st.session_state["goal"]= goal
    st.switch_page("pages/UserInputs.py")

#page 2
st.title("Help us know you")

#defined the variables
move_forward = st.selectbox("Do you want to answer some questions about yourself?",["no","yes"])
meal_appetizers=""
meal_entrees=""
meal_budget=0
#ask for user input + store them in variables
if move_forward == "yes" :
    st.text("Let us make your meal and your day")
    meal_appetizers = st.selectbox("How many appetizers do you want your meal to have? :", ["0","1","2","3","4"])
    meal_entrees = st.selectbox("How many entrees do you want your meal to have? :", ["0","1", "2", "3", "4"])
    meal_budget = st.number_input("What is the maximum amount of dollars you want your meal to be? :")
    st.text("To find the meal plan, press the button")
with st.form("my_form"):
    button_translate = st.form_submit_button("Meal Plan")
#this code gets the data from previous pages.
if button_translate:
    st.session_state["meal_appetizers"] = meal_appetizers
    st.session_state["meal_entrees"] = meal_entrees
    st.session_state["meal_budget"] = meal_budget
    st.switch_page("pages/MealPlan.py")




from pages.UserInputs import meal_appetizers, meal_entrees, meal_budget
from MainPage import name, goal, dietary_restrictions, kitchen_restrictions, caloric_max, meal_time

genai.configure(api_key=st.secrets["APIKEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("Meal Plan")
st.text("This is your meal plan")

def progressbar():
    # Initialize the progress bar
    progress_text = "Finding meal plan. Please wait."
    my_bar = st.progress(0, text=progress_text)

    # Simulate a long-running task with a loop
    for percent_complete in range(100):
        time.sleep(0.1)  # Simulate work being done
        my_bar.progress(percent_complete + 1, text=f"{progress_text} {percent_complete + 1}%")
    st.success("Meal Plan Found!")

prompt = f"""
You are an expert dietitian and you will help me design a meal plan.
You will be given restrictions as to what you can and can't do.

Their name is {st.session_state.get("name","")} and they want to eat for {st.session_state.get("goal","")}, so keep that in mind when designing thier meal plan.
They are a {st.session_state.get("dietary_restrictions","")} and are restricted by {st.session_state.get("kitchen_restrictions","")}.
They also want a maximum of {st.session_state.get("caloric_max","")} calories total for the entire meal.
They want a meal for {st.session_state.get("meal_time","")}.
As per the meal, they want {st.session_state.get("meal_appetizer","")} appetizer/s, and they want {meal_entrees} entrees.
They also have a maximum of{st.session_state.get("meal_budget","")} dollars.

So using this criteria, generate a meal plan that is versatile, do not include more that is asked.
"""

response = model.generate_content(prompt)
progressbar()
st.write(response.text)

if st.button("Switch to Main"):
    st.switch_page("../MainPage.pys")
