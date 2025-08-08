# Rupin Tham's code backbone
import streamlit as st
import google.generativeai as genai
import re

def run():
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    model = genai.GenerativeModel('gemini-2.5-flash')

    st.set_page_config(page_title="FreshFetch Meal Plan", layout="wide")
    st.title("FreshFetch Meal Plan Generator")

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0

    questions = [
        {"text": "1. What is the purpose of meal planning?", "key": "event"},
        {"text": "2. What is the duration of the plan (e.g., 7 days, 1 weekend)?", "key": "duration"},
        {"text": "3. Describe the desired setting or outcome:", "key": "setting"},
        {"text": "4. List mandatory restrictions/allergies (or 'None'):", "key": "restrictions"},
        {"text": "5. List dietary preferences and dislikes (or 'None'):", "key": "preferences"},
        {"text": "6. List any nutritional focus (or 'None'):", "key": "nutrition_focus"},
        {"text": "7. List any kitchen equipment constraints (or 'None'):", "key": "equipment"},
        {"text": "8. Enter your total grocery budget (e.g., $100 total):", "key": "budget"},
        {"text": "9. Optional: Describe your grocery shopping style (or leave blank):", "key": "shopping_style"},
    ]

    st.session_state.total_questions = len(questions)

    progress_percentage = st.session_state.current_question / st.session_state.total_questions
    st.progress(progress_percentage)

    if st.session_state.current_question < st.session_state.total_questions:
        current_q = questions[st.session_state.current_question]
        st.write(current_q["text"])
        st.text_input("Your Answer", key=current_q["key"])

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.current_question > 0:
            if st.button("Back"):
                st.session_state.current_question -= 1
                st.rerun()

    with col2:
        if st.session_state.current_question < st.session_state.total_questions:
            if st.session_state.get(questions[st.session_state.current_question]['key'], ''):
                if st.button("Next"):
                    st.session_state.current_question += 1
                    st.rerun()
        elif st.session_state.current_question == st.session_state.total_questions:
            if st.button("Generate Meal Plan"):
                prompt = f'''
As an experienced culinary artist, certified nutritionist, and registered dietitian, your primary objective is to craft a personalized, budget-conscious, and health-optimized meal plan, accompanied by a precise grocery list, tailored to my specific needs. My goal is to create exceptional and nourishing meals for the following event or situation.

1. Event & Context
- Purpose of Meal Planning: {st.session_state.get('event', 'N/A')}
- Duration of Plan: {st.session_state.get('duration', 'N/A')}
- Desired Setting: {st.session_state.get('setting', 'N/A')}

2. Dietary & Health Profile
- Mandatory Restrictions / Allergies: {st.session_state.get('restrictions', 'None')}
- Dietary Preferences & Dislikes: {st.session_state.get('preferences', 'None')}
- Nutritional Focus: {st.session_state.get('nutrition_focus', 'None')}
- Kitchen Equipment Constraints: {st.session_state.get('equipment', 'None')}

3. Budgetary Framework
- Total Grocery Budget: {st.session_state.get('budget', 'N/A')}
- Grocery Shopping Style: {st.session_state.get('shopping_style', 'None')}

4. Required Output

A. Detailed Meal Plan
- Dish Name & Brief Description
- Key Ingredients Highlight
- Estimated Prep & Cooking Time
- Portion Estimate
- Nutritional Rationale

B. Optimized Grocery List
- Categorization by grocery store section
- Precise Quantities
- Cost-Saving Notes

C. Chef's & Dietitian's Strategic Advice
- Budget Management Tips
- Preparation Efficiency
- Flexibility & Substitution Notes
- Nutritional Insights

Important Considerations for Your AI Analysis
- Creativity & Innovation
- Practicality
- Flavor Balance
- Minimize Waste

Please respond as a trusted and seasoned culinary-nutritional expert-professional, clear, warm, and fully aligned with my goals for nourishment, enjoyment, and practical success.
'''

                with st.spinner('Generating your personalized meal plan...'):
                    try:
                        response = model.generate_content(prompt)
                        generated_text = response.candidates[0].content.parts[0].text
                        st.session_state.generated_content = str(generated_text)  # Save to session state
                        st.rerun()  # <-- Force rerun to display result immediately
                    except Exception as e:
                        st.session_state.generated_content = None
                        st.error(f"Sorry, something went wrong while generating the meal plan. Error: {e}")

    if 'generated_content' in st.session_state and st.session_state.generated_content is not None:
        st.subheader("Your Personalized Meal Plan")

        try:
            content = st.session_state.generated_content

            meal_plan_match = re.search(r"A\. Detailed Meal Plan\s*(-.*?\n\n|\Z)", content, re.DOTALL)
            grocery_list_match = re.search(r"B\. Optimized Grocery List\s*(-.*?\n\n|\Z)", content, re.DOTALL)
            advice_match = re.search(r"C\. Chef's & Dietitian's Strategic Advice\s*(-.*|\Z)", content, re.DOTALL)

            meal_plan_content = meal_plan_match.group(1).strip() if meal_plan_match else "Could not generate Detailed Meal Plan."
            grocery_list_content = grocery_list_match.group(1).strip() if grocery_list_match else "Could not generate Optimized Grocery List."
            advice_content = advice_match.group(1).strip() if advice_match else "Could not generate Chef's & Dietitian's Strategic Advice."

            tab1, tab2, tab3 = st.tabs(["Detailed Meal Plan", "Optimized Grocery List", "Chef's & Dietitian's Strategic Advice"])

            with tab1:
                st.write(meal_plan_content)

            with tab2:
                st.write(grocery_list_content)

            with tab3:
                st.write(advice_content)

        except (IndexError, AttributeError) as e:
            st.error(f"Sorry, something went wrong with processing the generated response. Error: {e}")
