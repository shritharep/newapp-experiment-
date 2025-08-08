import streamlit as st
import google.generativeai as genai
import time  

def run():
    # Configure Gemini API
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Set page config
    st.set_page_config(page_title="Fresh Fetch", layout="wide")

    # Welcome header
    st.markdown("<h1 style='text-align: center; color: black;'>Selective Meal Plan</h1>", unsafe_allow_html=True)
    st.text("Welcome to...")

    # Define options
    dietary_options = ["Vegan", "Vegetarian", "Non-Vegetarian", "Pescatarian", "Omnivore"]
    meal_preptime = ["All Day", "Breakfast", "Brunch", "Lunch", "Dinner"]

    # Collect basic user input
    name = st.text_input("Enter your name")
    dietary_restrictions = st.selectbox("What are your dietary restrictions?", dietary_options)
    meal_time = st.selectbox("What is your meal time?", meal_preptime)
    kitchen_restrictions = st.text_input("What are your kitchen restrictions? (e.g. materials you lack)")
    goal = st.text_input("Enter your goal or purpose for this meal")
    caloric_max = st.number_input("Maximum calories for the full meal:")

    # Optional deeper questions
    st.title("Help us know you better")

    move_forward = st.selectbox("Do you want to answer some questions about yourself?", ["no", "yes"])
    meal_appetizers = "0"
    meal_entrees = "0"
    meal_budget = 0

    if move_forward == "yes":
        st.text("Let us make your meal and your day.")
        meal_appetizers = st.selectbox("How many appetizers do you want?", ["0", "1", "2", "3", "4"])
        meal_entrees = st.selectbox("How many entrees do you want?", ["0", "1", "2", "3", "4"])
        meal_budget = st.number_input("What is your meal budget (in dollars)?")

    # Submit button to save to session state and generate prompt
    if st.button("Generate Meal Plan"):
        st.session_state["name"] = name
        st.session_state["goal"] = goal
        st.session_state["dietary_restrictions"] = dietary_restrictions
        st.session_state["kitchen_restrictions"] = kitchen_restrictions
        st.session_state["caloric_max"] = caloric_max
        st.session_state["meal_time"] = meal_time
        st.session_state["meal_appetizers"] = meal_appetizers
        st.session_state["meal_entrees"] = meal_entrees
        st.session_state["meal_budget"] = meal_budget

        # Generate prompt
        prompt = f"""
        You are an expert dietitian and chef.
        Help design a meal plan for {name} who is planning a meal for the purpose of: {goal}.
        - Dietary type: {dietary_restrictions}
        - Kitchen constraints: {kitchen_restrictions}
        - Meal time: {meal_time}
        - Max calories: {caloric_max}
        - Appetizers requested: {meal_appetizers}
        - Entrees requested: {meal_entrees}
        - Max budget: ${meal_budget}

        Please generate a plan with only the requested number of items, keeping it versatile, healthy, and practical.
        """

        # Show spinner & progress bar
        with st.spinner("Generating meal plan..."):
            try:
                response = model.generate_content(prompt)
                plan_text = response.text

                # Simulated progress bar
                progress_text = "Finding meal plan. Please wait."
                my_bar = st.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.01)  # Faster for demo
                    my_bar.progress(percent_complete + 1, text=f"{progress_text} {percent_complete + 1}%")
                st.success("Meal Plan Found!")

                st.subheader("Your Meal Plan")
                st.write(plan_text)

            except Exception as e:
                st.error(f"Error generating meal plan: {e}")

    # Optional: back to main/home button
    if st.button("Back to Main"):
        st.switch_page("MainPage.py")
