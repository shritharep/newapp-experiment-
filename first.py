import streamlit as st
import google.generativeai as genai

def run():
    genai.configure(api_key=st.secrets["APIKEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")

    st.header("Individual Wellness Planner")
    st.write("Welcome to your very own customized wellness guide, tailored to you and your needs!")

    name = st.text_input("What is your name, or what should we call you?")
    if name:
        st.success(f"Hi {name}! Welcome to the community! Let's get started.")

        dietary_lifestyle = st.text_input("What is your dietary lifestyle? (e.g., vegetarian, vegan, non-vegetarian, no restrictions)")

        goals = st.selectbox("What is your aim with this platform?", ["", "fitness", "health", "weight-management"])
    
        specific = ""
        particular = ""

        if goals:
            if goals == "fitness":
                st.info("Looks like you want to improve your fitness levels. Good for you!")
            elif goals == "health":
                st.info("Looks like you want to improve your health. Good for you!")
            elif goals == "weight-management":
                st.info("Looks like you want to work on your weight. Good for you!")

            specific = st.text_input("What is your specific goal?")
            particular = st.text_input("Any specific area of your body or any further specifications?")

            goal_date = st.date_input("What is your goal date?", format="MM/DD/YYYY")
            investment = st.text_input("How much are you willing to invest per month? (e.g., $100-$200)")

            age = st.number_input("Lastly, what is your age?", min_value=0, step=1)

            if age > 0:
                if age <= 1:
                    st.info("You are in the infant category.")
                elif age < 13:
                    st.info("You are in the child category.")
                elif age < 18:
                    st.info("You are in the teenager category.")
                else:
                    st.info("You fall under the adult category.")

            if st.button("Generate My Plan"):
                details = {
                    "Dietary Lifestyle": dietary_lifestyle,
                    "Goal(s)": goals,
                    "Specific Goal": specific,
                    "Particular Notes/Specifications": particular,
                    "Projected Goal Date": goal_date.strftime("%m/%d/%Y"),
                    "Preferred Investment Range": investment,
                    "Age": age
                }

                st.subheader("Here is what you provided:")
                st.json(details)

                prompt = f"""
                    You are my personal dietitian and trainer, tailoring my dietary needs and restrictions to provide personalized meal plans.
                    Provide advice to help me meet my goals. Include a suggested calorie count, and a weekly planner of what I should be eating or doing to achieve my goals by {goal_date}.
                    Provide the output in plain text. Do not use any markdown formatting, including headings, lists, bold text, or underlining. Structure the information clearly using line breaks and indentation only. Use bullet points under subheadings with hyphens.

                    Here is the information about me from the provided data:
                    Dietary Lifestyle: {dietary_lifestyle}
                    Age: {age}
                    Goal(s): {goals}
                    Specific Goal: {specific}
                    Further Specifications: {particular}
                    Projected Goal Date: {goal_date.strftime('%m/%d/%Y')}
                    Preferred Investment Range: {investment}

                    Based on this info, I am {age} years old, and my dietary lifestyle is {dietary_lifestyle}. My goal date is {goal_date.strftime('%m/%d/%Y')}, and I'm willing to invest {investment} per month. I want to work on my {goals}, specifically {specific}. I also have some further notes and specifications: {particular}.
                """

                response = model.generate_content([prompt])
                st.subheader("Your Customized Plan:")
                st.text(response.text)
            else:
                st.warning("Please fill in all the fields to generate your personalized plan.")
    else:
        st.warning("Please enter your name to start.")
