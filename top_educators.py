import streamlit as st
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import os
import google.generativeai as genai  
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")  
    if not api_key:
        st.error("Google API Key not found. Please check your .env file.")
        st.stop()

    genai.configure(api_key=api_key)
    chat_model = genai.GenerativeModel("gemini-1.5-flash")

    # Function to load and process dataset
    def load_data(file_path):
        try:
            df = pd.read_csv(file_path, encoding='latin1')
            df["combined_text"] = df.apply(lambda row: " ".join(row.values.astype(str)), axis=1)
            
            # Load embedding model
            model = SentenceTransformer("all-MiniLM-L6-v2")
            embeddings = model.encode(df["combined_text"].tolist())
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)
            
            return df, index, model, embeddings
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.stop()

    # Load CSV directly from server
    csv_file_path = "educators_mentors_dataset_.csv"
    if not os.path.exists(csv_file_path):
        st.error(f"CSV file not found at {csv_file_path}. Please upload it to the server.")
        st.stop()

    df, index, model, embeddings = load_data(csv_file_path)

    # Streamlit UI setup
    st.title("🔍 AI-Powered Profile Search & Assistant Chatbot")

    # Search bar
    query = st.text_input("Enter search query (e.g., 'I need a mentor for Generative AI'):")
    if st.button("Search"):
        if query:
            query_embedding = model.encode([query])
            k = 5
            distances, indices = index.search(query_embedding, k)
            
            # Display results
            st.subheader("🎯 Top 5 Matching Educators")
            for idx in indices[0]:
                profile = df.iloc[idx]
                st.write(f"**👤 Name:** {profile['Name']}")
                st.write(f"**🌐 Website:** {profile['Website']}")
                st.write(f"**📧 Email:** {profile['Email']}")
                st.write(f"**🛠 Expertise:** {profile['Expertise']}")
                st.write(f"**📆 Years of Experience:** {profile['Years_of_Experience']} years")
                st.markdown("---")  # Separator
        else:
            st.warning("Please enter a search query.")

    # Assistant Chatbot
    st.subheader("🤖 Assistant Chatbot")
    user_input = st.text_input("Ask Assistant about networking, career, or interests:")
    if st.button("Chat with Assistant"):
        if user_input:
            response = chat_model.generate_content(user_input)
            st.write("**Assistant:**")
            st.write(response.text)
        else:
            st.warning("Please enter a question for the assistant.")

if __name__ == "__main__":
    main()
