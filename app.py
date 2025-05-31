import streamlit as st
import requests
import http
import os
from dotenv import load_dotenv

load_dotenv()



# Gemini API Key
GEMINI_API_KEY  st.secrets["JEUN_API_KEY"]

# Gemini API endpoint
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_meal_plan(culture, taste, health_conditions, allergies, duration):
    prompt = (
        f"Create a {duration}-day meal plan for a user from {culture} culture "
        f"who enjoys {taste} foods, has the following health challenges: {health_conditions}, "
        f"and is allergic to {allergies}. "
        f"let this meal plan be in tabular form. that is, monday through saturday and have headers:breakfast, lunch and dinner."

    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print("Response text:", response.text)
        content = response.json()
        return content["candidates"][0]["content"]["parts"][0]["text"]
   
    else:
        st.error("Error from Gemini API:")
        return None


# Streamlit UI
st.title("🥗 AI Meal Planner with Gemini")

st.markdown("Get a personalized meal plan based on your culture, taste, and health!")

culture = st.selectbox("🌍 Culture", ["Nigerian", "Indian", "American", "Mediterranean", "Custom"])
if culture == "Custom":
    culture = st.text_input("Enter custom culture")

taste = st.multiselect("🍽️ Taste Preferences", ["Spicy", "Sweet", "Savory", "Bland", "Sour", "Bitter"])

health_conditions = st.text_input("🩺 Health Challenges (e.g., diabetes, hypertension)")
allergies = st.text_input("🚫 Allergies (e.g., nuts, dairy)")
duration = st.slider("📅 Plan Duration (days)", 1, 7, 3)

if st.button("Generate Meal Plan"):
    with st.spinner("Cooking up your custom meal plan..."):
        plan = generate_meal_plan(culture, ", ".join(taste), health_conditions, allergies, duration)
        if plan:
            st.success("Meal plan generated successfully!")
            st.markdown(plan)
