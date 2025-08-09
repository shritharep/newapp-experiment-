# Rithikk Vimal's code backbone
import streamlit as st
import google.generativeai as genai
import time  

def run():
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')

    st.set_page_config(page_title="FreshFetch", layout="wide")
    st.markdown("<h2 style='text-align: center; color: black;'>Selective Meal Planner</h2>", unsafe_allow_html=True)

    dietary_options = ["Vegan", "Vegetarian", "Non-Vegetarian", "Pescatarian", "Omnivore"]
    meal_preptime = ["All Day", "Breakfast", "Brunch", "Lunch", "Dinner"]

    if "questions_answered" not in st.session_state:
        st.session_state["questions_answered"] = 0
    if "progress_completed" not in st.session_state:
        st.session_state["progress_completed"] = False
    if "move_forward" not in st.session_state:
        st.session_state["move_forward"] = "no"

    def get_total_questions():
        return 10 if st.session_state.get("move_forward") == "yes" else 7

    total_questions = get_total_questions()
    percent = int((st.session_state["questions_answered"] / total_questions) * 100)
    progress_placeholder = st.empty()
    progress_bar = progress_placeholder.progress(percent, text=f"Progress: {percent}%")

    def update_progress():
        total = get_total_questions()
        percent = int((st.session_state["questions_answered"] / total) * 100)
        progress_bar.progress(percent, text=f"Progress: {percent}%")

    name = st.text_input("Enter your name", key="name")
    if name:
        st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 1)
    update_progress()

    dietary_restrictions = st.selectbox("What are your dietary restrictions?", dietary_options, key="dietary_restrictions")
    if dietary_restrictions:
        st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 2)
    update_progress()

    meal_time = st.selectbox("What is your meal time?", meal_preptime, key="meal_time")
    if meal_time:
        st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 3)
    update_progress()

    kitchen_restrictions = st.text_input("What are your kitchen restrictions? (e.g. materials you lack)", key="kitchen_restrictions")
    if kitchen_restrictions is not None:
        st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 4)
    update_progress()

    goal = st.text_input("Enter your goal or purpose for this meal", key="goal")
    if goal:
        st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 5)
    update_progress()

    caloric_max = st.number_input("Maximum calories for the full meal:", key="caloric_max")
    st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 6)
    update_progress()

    st.title("Help us know you better")

    move_forward = st.selectbox("Do you want to answer some questions about yourself?", ["no", "yes"], key="move_forward")
    if move_forward:
        st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 7)
    update_progress()

    meal_appetizers = "0"
    meal_entrees = "0"
    meal_budget = 0

    if move_forward == "yes":
        st.text("Let us make your meal and your day.")
        meal_appetizers = st.selectbox("How many appetizers do you want?", ["0", "1", "2", "3", "4"], key="meal_appetizers")
        if meal_appetizers:
            st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 8)
        update_progress()

        meal_entrees = st.selectbox("How many entrees do you want?", ["0", "1", "2", "3", "4"], key="meal_entrees")
        if meal_entrees:
            st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 9)
        update_progress()

        meal_budget = st.number_input("What is your meal budget (in dollars)?", key="meal_budget")
        st.session_state["questions_answered"] = max(st.session_state["questions_answered"], 10)
        update_progress()
    else:
        st.session_state["progress_completed"] = True
        update_progress()

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

        with st.spinner("Generating meal plan..."):
            try:
                response = model.generate_content(prompt)
                plan_text = response.candidates[0].content.parts[0].text

                st.success("Meal Plan Found!")
                st.subheader("Your Meal Plan")
                st.write(plan_text)

            except Exception as e:
                st.error(f"Error generating meal plan: {e}")

if __name__ == "__main__":
    run()
