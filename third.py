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

    if "move_forward" not in st.session_state:
        st.session_state["move_forward"] = "no"

    def get_total_questions():
        return 10 if st.session_state.get("move_forward") == "yes" else 7

    # Collect responses first
    name = st.text_input("Enter your name", key="name")
    dietary_restrictions = st.selectbox("What are your dietary restrictions?", dietary_options, key="dietary_restrictions")
    meal_time = st.selectbox("What is your meal time?", meal_preptime, key="meal_time")
    kitchen_restrictions = st.text_input("What are your kitchen restrictions? (e.g. materials you lack)", key="kitchen_restrictions")
    goal = st.text_input("Enter your goal or purpose for this meal", key="goal")
    caloric_max = st.number_input("Maximum calories for the full meal:", key="caloric_max")
    st.title("Help us know you better")
    move_forward = st.selectbox("Do you want to answer some questions about yourself?", ["no", "yes"], key="move_forward")

    meal_appetizers = meal_entrees = meal_budget = None
    if move_forward == "yes":
        st.text("Let us make your meal and your day.")
        meal_appetizers = st.selectbox("How many appetizers do you want?", ["0", "1", "2", "3", "4"], key="meal_appetizers")
        meal_entrees = st.selectbox("How many entrees do you want?", ["0", "1", "2", "3", "4"], key="meal_entrees")
        meal_budget = st.number_input("What is your meal budget (in dollars)?", key="meal_budget")

    # Count answered questions (only if filled)
    answered = 0
    if name: answered += 1
    if dietary_restrictions: answered += 1
    if meal_time: answered += 1
    # kitchen_restrictions can be empty, but we still count it as answered (since it's optional)
    answered += 1
    if goal: answered += 1
    # caloric_max has a default (0), so check if the user changed it or just always count it
    answered += 1
    if move_forward: answered += 1
    if move_forward == "yes":
        if meal_appetizers: answered += 1
        if meal_entrees: answered += 1
        # meal_budget is number_input, always counts as answered
        answered += 1

    total_questions = get_total_questions()
    percent = int((answered / total_questions) * 100)
    progress_placeholder = st.empty()
    progress_bar = progress_placeholder.progress(percent, text=f"Progress: {percent}%")

    if st.button("Generate Meal Plan"):
        st.session_state["name"] = name
        st.session_state["goal"] = goal
        st.session_state["dietary_restrictions"] = dietary_restrictions
        st.session_state["kitchen_restrictions"] = kitchen_restrictions
        st.session_state["caloric_max"] = caloric_max
        st.session_state["meal_time"] = meal_time
        st.session_state["meal_appetizers"] = meal_appetizers or "0"
        st.session_state["meal_entrees"] = meal_entrees or "0"
        st.session_state["meal_budget"] = meal_budget or 0

        prompt = f"""
        You are an expert dietitian and chef.
        Help design a meal plan for {name} who is planning a meal for the purpose of: {goal}.
        - Dietary type: {dietary_restrictions}
        - Kitchen constraints: {kitchen_restrictions}
        - Meal time: {meal_time}
        - Max calories: {caloric_max}
        - Appetizers requested: {meal_appetizers or "0"}
        - Entrees requested: {meal_entrees or "0"}
        - Max budget: ${meal_budget or 0}

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
