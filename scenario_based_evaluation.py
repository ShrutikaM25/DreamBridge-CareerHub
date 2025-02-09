import io
import streamlit as st
import fitz  # PyMuPDF for parsing PDF
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

# Load API key from environment variable
def main():
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

    # Initialize the Groq LLM
    llm = ChatGroq(
        model_name="mixtral-8x7b-32768",
        groq_api_key=GROQ_API_KEY,
        temperature=0.7
    )

    # Function to extract text from a PDF file-like object
    def extract_text_from_pdf(file):
        # Open the file-like object using PyMuPDF
        doc = fitz.open(stream=file.read(), filetype="pdf")
        full_text = []
        for page in doc:
            full_text.append(page.get_text())
        return '\n'.join(full_text)

    # ================================
    # 1️⃣ Scenario Generation Chain
    # ================================
    scenario_prompt = PromptTemplate(
        input_variables=["profile"],
        template="Based on the following candidate profile:\n{profile}\nGenerate a realistic work scenario."
    )
    scenario_chain = scenario_prompt | llm

    # ================================
    # 2️⃣ Interactive Follow-Up Chain
    # ================================
    followup_prompt = PromptTemplate(
        input_variables=["scenario", "response"],
        template="Given this work scenario: {scenario}\nThe candidate responded: {response}\nGenerate a follow-up question to continue the discussion."
    )
    followup_chain = followup_prompt | llm

    # ================================
    # 3️⃣ Evaluation Chain
    # ================================
    evaluation_prompt = PromptTemplate(
        input_variables=["scenario", "response"],
        template=(
            "Scenario: {scenario}\n"
            "Candidate Response: {response}\n\n"
            "Evaluate the response based on the following criteria:\n\n"
            "### 🏆 Problem-Solving Ability\n"
            "**Score:** (1-10)\n"
            "**Justification:**\n\n"
            "### 💡 Technical Accuracy\n"
            "**Score:** (1-10)\n"
            "**Justification:**\n\n"
            "### 🎨 Creativity\n"
            "**Score:** (1-10)\n"
            "**Justification:**\n\n"
            "### 🗣 Communication Clarity\n"
            "**Score:** (1-10)\n"
            "**Justification:**\n\n"
            "Ensure that the response is structured clearly under each heading."
        )
    )

    evaluation_chain = evaluation_prompt | llm

    st.title("🧑‍💻 AI-Powered Candidate Evaluation")

    # Upload Resume (PDF)
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

    # **Persist scenario in session state**
    if "scenario" not in st.session_state:
        st.session_state.scenario = None

    # Extract profile from resume if file uploaded
    if resume_file:
        resume_text = extract_text_from_pdf(resume_file)
        # Displaying first 1000 characters for preview
    else:
        resume_text = ""

    # ================================
    # Profile for Scenario Generation
    # ================================
    candidate_profile = st.text_area("Enter Candidate Profile:", 
                                    resume_text , height=200)

    # **Ensure scenario remains available before generating scenario**
    if "scenario" not in st.session_state:
        st.session_state.scenario = None

    # Generate scenario button
    if st.button("Generate Scenario"):
        with st.spinner("Generating work scenario..."):
            st.session_state.scenario = scenario_chain.invoke({"profile": candidate_profile}).content

    # Display the scenario (if generated)
    if st.session_state.scenario:
        st.subheader("📌 Generated Work Scenario:")
        st.write(st.session_state.scenario)

    # Input for candidate response
    candidate_response = st.text_area("Enter Candidate Response:", 
                                    "I would approach the task by first understanding the requirements, designing a modular solution, and ensuring efficiency in the implementation.")

    # **Ensure the scenario remains available before evaluating**
    if st.session_state.scenario:
        # Evaluate Response
        if st.button("Evaluate Response"):
            with st.spinner("Evaluating response..."):
                evaluation_result = evaluation_chain.invoke({
                    "scenario": st.session_state.scenario, 
                    "response": candidate_response
                })
                evaluation_content = evaluation_result.content if hasattr(evaluation_result, 'content') else "Error: Evaluation not generated."

            st.subheader("📊 Evaluation Results:")
            st.markdown(evaluation_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()