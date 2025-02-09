import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from dotenv import load_dotenv
from datetime import datetime
import json

def main():
    # Load API key from environment variable
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    if "roadmaps" not in st.session_state:
        st.session_state.roadmaps = []

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Please add it to your environment variables.")

    # Initialize LLM model with API key
    llm = ChatGroq(model_name="mixtral-8x7b-32768", groq_api_key=GROQ_API_KEY, temperature=0.5)

    # Custom CSS for better UI
    st.markdown("""
    <style>
        .main-container {
            background: linear-gradient(135deg, #1a2a4a 0%, #0d1b2a 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            color: white;
            margin-bottom: 10px;
        }
        .main-container:hover {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        .stButton button {
            border-radius: 10px;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            transition: 0.3s ease-in-out;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextInput input, .stSelectbox select, .stTextArea textarea {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

    def generate_roadmap(user_input):
        prompt = f"""
        Based on the following user details:
        {user_input}

        Create a comprehensive career development plan including:

        1. Career Summary:
        - Overview of potential career directions
        - Market demand analysis
        - Salary ranges

        2. Skill Development Plan:
        - Technical skills needed
        - Soft skills required
        - Priority order for skill acquisition

        3. Education and Certification Roadmap:
        - Recommended certifications
        - Online courses with links
        - Expected completion timeframes

        4. Career Progression Timeline:
        - Entry-level positions
        - Mid-level roles
        - Senior positions
        - Timeline estimates

        5. Industry Focus:
        - Primary industry recommendations
        - Alternative industries
        - Growth sectors analysis

        6. Networking Strategy:
        - Professional organizations
        - Industry events
        - Online communities

        7. Project Portfolio Recommendations:
        - Suggested projects
        - Skills to demonstrate
        - Portfolio presentation tips

        8. Short-term Goals (0-2 years):
        - Specific actionable goals
        - Learning objectives
        - Career milestones

        9. Medium-term Goals (2-5 years):
        - Role progression
        - Skill mastery targets
        - Industry positioning

        10. Long-term Goals (5+ years):
        - Leadership opportunities
        - Industry influence
        - Career achievement targets

        Please provide detailed, actionable insights for each section.
        """
        return llm.invoke(prompt)

    tools = [
        Tool(
            name="Career Roadmap Generator",
            func=generate_roadmap,
            description="Generates a comprehensive career roadmap based on user inputs and career goals."
        )
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Streamlit UI
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("🔙 Back", key="back_to_dashboard"):
            st.session_state.page = "home"

    st.markdown("""
        <div class="main-container">
            <h1>🚀 Career Roadmap Generator</h1>
            <p>Create your personalized career development plan with AI-powered insights</p>
        </div>
    """, unsafe_allow_html=True)

    # Use form to keep values between interactions
    with st.form(key="career_form"):
        # User Profile Section
        st.markdown("### 👤 Your Professional Profile")
        
        col1, col2 = st.columns(2)
        with col1:
            current_role = st.text_input("Current Role", placeholder="e.g., Software Developer", value=st.session_state.get('current_role', ''))
            experience_years = st.slider("Years of Experience", 0, 20, 2, key="experience_years")
            education = st.selectbox(
                "Education Level",
                ["High School", "Bachelor's", "Master's", "PhD", "Other Certifications"],
                index=["High School", "Bachelor's", "Master's", "PhD", "Other Certifications"].index(st.session_state.get('education', "Bachelor's"))
            )

        with col2:
            location = st.text_input("Location", placeholder="e.g., New York, USA", value=st.session_state.get('location', ''))
            work_type = st.multiselect(
                "Preferred Work Type",
                ["Remote", "Hybrid", "On-site", "Flexible"],
                default=st.session_state.get('work_type', [])
            )
            salary_range = st.select_slider(
                "Target Salary Range (K USD)",
                options=['0-50', '50-75', '75-100', '100-150', '150-200', '200+'],
                value=st.session_state.get('salary_range', '50-75')
            )

        # Skills and Interests
        st.markdown("### 🎯 Skills & Interests")
        
        col1, col2 = st.columns(2)
        with col1:
            technical_skills = st.text_area(
                "Technical Skills",
                placeholder="e.g., Python, SQL, AWS...",
                help="Enter skills separated by commas",
                value=st.session_state.get('technical_skills', '')
            )
            soft_skills = st.text_area(
                "Soft Skills",
                placeholder="e.g., Leadership, Communication...",
                help="Enter skills separated by commas",
                value=st.session_state.get('soft_skills', '')
            )

        with col2:
            interests = st.text_area(
                "Professional Interests",
                placeholder="e.g., Machine Learning, Web Development...",
                help="Enter interests separated by commas",
                value=st.session_state.get('interests', '')
            )
            industries = st.multiselect(
                "Target Industries",
                ["Technology", "Finance", "Healthcare", "Education", "Marketing", 
                 "Manufacturing", "Consulting", "Retail", "Energy", "Entertainment"],
                default=st.session_state.get('industries', [])
            )

        # Career Goals
        st.markdown("### 🎯 Career Goals")
        
        short_term = st.text_area("Short-term Goals (0-2 years)", placeholder="What do you want to achieve in the next 2 years?", value=st.session_state.get('short_term', ''))
        medium_term = st.text_area("Medium-term Goals (2-5 years)", placeholder="Where do you see yourself in 5 years?", value=st.session_state.get('medium_term', ''))
        long_term = st.text_area("Long-term Goals (5+ years)", placeholder="What's your ultimate career aspiration?", value=st.session_state.get('long_term', ''))

        # Additional Preferences
        st.markdown("### 🔍 Additional Preferences")
        
        col1, col2 = st.columns(2)
        with col1:
            learning_style = st.multiselect(
                "Preferred Learning Style",
                ["Self-paced online courses", "Structured programs", "Hands-on projects", 
                 "Mentorship", "Academic education"],
                default=st.session_state.get('learning_style', [])
            )
            work_culture = st.multiselect(
                "Preferred Work Culture",
                ["Startup", "Corporate", "Agency", "Consulting", "Research", "Non-profit"],
                default=st.session_state.get('work_culture', [])
            )

        with col2:
            career_priorities = st.multiselect(
                "Career Priorities",
                ["Work-life balance", "High salary", "Learning opportunities", 
                 "Leadership roles", "Innovation", "Social impact"],
                default=st.session_state.get('career_priorities', [])
            )

        # Submit form button
        submit_button = st.form_submit_button("Generate Career Roadmap")

        if submit_button:
            with st.spinner("Generating your personalized career roadmap..."):
                user_input = {
                    "input": {  # Add 'input' key to match the expected format
                        "profile": {
                            "current_role": current_role,
                            "experience": experience_years,
                            "education": education,
                            "location": location,
                            "work_type": work_type,
                            "salary_range": salary_range
                        },
                        "skills": {
                            "technical": technical_skills.split(","),
                            "soft": soft_skills.split(",")
                        },
                        "interests": interests.split(","),
                        "industries": industries,
                        "goals": {
                            "short_term": short_term,
                            "medium_term": medium_term,
                            "long_term": long_term
                        },
                        "preferences": {
                            "learning_style": learning_style,
                            "work_culture": work_culture,
                            "priorities": career_priorities
                        }
                    }
                }

                response = agent.run(user_input)
                st.session_state.response = response

                # Append the generated roadmap to the session state
                st.session_state.roadmaps.append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "data": response
                })

                st.success("Career roadmap generated successfully!")

            if response.startswith("{") and response.endswith("}"):
                try:
                    parsed_response = json.loads(response)
                    st.json(parsed_response)
                except json.JSONDecodeError:
                    st.markdown(f"### Career Roadmap Output:\n\n{response}")
            else:
                st.markdown(f"### Career Roadmap Output:\n\n{response}")

    if len(st.session_state.roadmaps) > 1:
        st.markdown("### 📚 Previous Roadmaps")
        for i, roadmap in enumerate(reversed(st.session_state.roadmaps[:-1])):
            with st.expander(f"Roadmap from {roadmap['date']}"):
                st.text(roadmap['data'])

        def download_json(data, filename="career_roadmap.json"):
            try:
                json_data = json.dumps(data, indent=4)
                st.download_button(
                    label="Download Roadmap JSON",
                    data=json_data,
                    file_name=filename,
                    mime="application/json"
                )
            except (TypeError, OverflowError) as e:
                st.error(f"Error generating JSON file: {str(e)}")


        download_json(st.session_state.roadmaps)

        if len(st.session_state.roadmaps) > 1:
            st.markdown("### 📚 Previous Roadmaps")
            for i, roadmap in enumerate(reversed(st.session_state.roadmaps[:-1])):
                with st.expander(f"Roadmap from {roadmap['date']}"):
                    st.text(roadmap['data'])


if __name__ == "__main__":
    main()
