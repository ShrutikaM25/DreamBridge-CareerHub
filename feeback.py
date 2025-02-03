import streamlit as st
import pandas as pd
import datetime
import os
from textblob import TextBlob

# CSV file for storing feedback
FEEDBACK_FILE = "feedback.csv"

# Initialize CSV if it doesn't exist
if not os.path.exists(FEEDBACK_FILE):
    df = pd.DataFrame(columns=["timestamp", "user", "feature", "rating", "usefulness", "accuracy", "ease_of_use", "recommend", "improvements", "comments", "sentiment"])
    df.to_csv(FEEDBACK_FILE, index=False)

st.title("📢 Feedback Form")
st.markdown("We appreciate your feedback to improve our system! 💡")

# User Inputs
user_name = st.text_input("Your Name (Optional):", "")
feature_type = st.selectbox("Which feature are you reviewing?", 
                          ["ATS Tracker", "Career Roadmap", "Market Analysis", "Skill Assessment"])
rating = st.slider("⭐ Overall Rating (1-5)", 1, 5, 3)

# Detailed Feedback Questions
usefulness = st.slider("🎯 How useful was this feature for your needs? (1-5)", 1, 5, 3)
accuracy = st.slider("🔍 How accurate were the results? (1-5)", 1, 5, 3)
ease_of_use = st.slider("🎛️ How easy was it to use? (1-5)", 1, 5, 3)
recommend = st.radio("👍 Would you recommend this feature to others?", ["Yes", "No", "Not Sure"])

# Open-ended Feedback
improvements = st.text_area("🔧 What improvements would you like to see?")
comments = st.text_area("💬 Any additional feedback or suggestions?")

if st.button("Submit Feedback"):
    if feature_type and rating and comments:
        # Load existing feedback
        df = pd.read_csv(FEEDBACK_FILE)

        # Perform sentiment analysis on comments
        sentiment_score = TextBlob(comments).sentiment.polarity
        sentiment = "Positive" if sentiment_score > 0 else "Neutral" if sentiment_score == 0 else "Negative"

        # Append new feedback
        new_feedback = pd.DataFrame([{
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "user": user_name,
            "feature": feature_type,
            "rating": rating,
            "usefulness": usefulness,
            "accuracy": accuracy,
            "ease_of_use": ease_of_use,
            "recommend": recommend,
            "improvements": improvements,
            "comments": comments,
            "sentiment": sentiment
        }])

        df = pd.concat([df, new_feedback], ignore_index=True)
        df.to_csv(FEEDBACK_FILE, index=False)  

        st.success("✅ Thank you! Your feedback has been recorded.")
    else:
        st.error("⚠️ Please provide a rating and feedback.")
