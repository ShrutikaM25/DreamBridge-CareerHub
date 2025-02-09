import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import google.generativeai as genai
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Google AI API
def init_google_api():
    api_key = "AIzaSyBYfzDovXQK6E8jZsrOBieoSY_X6jCUktU"

    genai.configure(api_key=api_key)
    chat_model = genai.GenerativeModel("gemini-1.5-flash")
    return chat_model

# Function to create SQLite database and store vectors
def create_local_database(file_path):
    try:
        # Load CSV file
        df = pd.read_csv(file_path, encoding='latin1')
        df["combined_text"] = df.apply(lambda row: " ".join(row.values.astype(str)), axis=1)
        
        # Create SQLite database
        conn = sqlite3.connect('vectors.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS embeddings
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, vector BLOB, text TEXT)''')

        # Initialize SentenceTransformer model
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(df["combined_text"].tolist())

        # Store vectors in SQLite database
        for i, embedding in enumerate(embeddings):
            c.execute("INSERT INTO embeddings (vector, text) VALUES (?, ?)", 
                      (embedding.tobytes(), df["combined_text"].iloc[i]))

        conn.commit()
        conn.close()

        return df, model
    except Exception as e:
        st.error(f"Error processing data: {e}")
        st.stop()

# Function to perform search using cosine similarity
def search_query(query, model, df):
    query_embedding = model.encode([query])[0]
    
    # Open the SQLite database to fetch the stored vectors
    conn = sqlite3.connect('vectors.db')
    c = conn.cursor()
    c.execute("SELECT id, vector, text FROM embeddings")
    rows = c.fetchall()
    conn.close()
    
    # Calculate cosine similarity between the query and the stored vectors
    stored_vectors = [np.frombuffer(row[1], dtype=np.float32) for row in rows]
    stored_texts = [row[2] for row in rows]
    
    # Compute cosine similarity
    similarities = cosine_similarity([query_embedding], stored_vectors)[0]
    
    # Get the top 5 most similar entries
    top_indices = similarities.argsort()[-5:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            "Name": stored_texts[idx].split(' ')[0],  # Assuming 'Name' is the first word
            "Expertise": stored_texts[idx],  # Assuming 'Expertise' is the entire text
            "Similarity": similarities[idx]
        })

    return results

# Main function to run the Streamlit application
def main():
    chat_model = init_google_api()

    # File path for CSV data
    csv_file_path = "educators_mentors_dataset_.csv"
    if not os.path.exists(csv_file_path):
        st.error(f"CSV file not found at {csv_file_path}. Please upload it.")
        st.stop()

    df, model = create_local_database(csv_file_path)

    # Streamlit UI setup
    st.title("🔍 AI-Powered Profile Search & Assistant Chatbot")

    # Search bar
    query = st.text_input("Enter search query (e.g., 'I need a mentor for Generative AI'):")
    if st.button("Search"):
        if query:
            results = search_query(query, model, df)
            
            st.subheader("🎯 Top 5 Matching Educators")
            for result in results:
                st.write(f"👤 Name: {result['Name']}")
                st.write(f"🛠 Expertise: {result['Expertise']}")
                st.write(f"🔍 Similarity Score: {result['Similarity']:.2f}")
                st.markdown("---")  # Separator
        else:
            st.warning("Please enter a search query.")

    # Assistant Chatbot
    st.subheader("🤖 Assistant Chatbot")
    user_input = st.text_input("Ask Assistant about networking, career, or interests:")
    if st.button("Chat with Assistant"):
        if user_input:
            response = chat_model.generate_content(user_input)
            st.write("Assistant:")
            st.write(response.text)
        else:
            st.warning("Please enter a question for the assistant.")

if _name_ == "_main_":
    main()