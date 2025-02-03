import streamlit as st
import pandas as pd
import numpy as np
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import plotly.express as px
import plotly.graph_objs as go

class SkillAssessment:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        
        # Initialize AI model
        self.llm = ChatGroq(
            model_name="mixtral-8x7b-32768", 
            groq_api_key=GROQ_API_KEY, 
            temperature=0.7
        )

    def generate_custom_css(self):
        return """
        <style>
            body {
                background: #1a202c; /* Dark background */
                color: white;
                font-family: Arial, sans-serif;
            }
            .skill-container {
                background: linear-gradient(135deg, #2d3748, #4a5568); /* Dark gradient */
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
            .assessment-card {
                background: #2d3748; /* Dark background for cards */
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }
            .assessment-card:hover {
                transform: scale(1.05);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            }
            .skill-radar {
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background: #2d3748; /* Dark background for radar chart */
                padding: 1rem;
                border-radius: 15px;
            }
            .skill-progress {
                background: linear-gradient(to right, #4299E1, #3182CE);
                border-radius: 10px;
                transition: width 0.5s ease-in-out;
            }
            h1, h2, h3, h4, p {
                color: #e2e8f0; /* Light text for headings and paragraphs */
            }
            .stButton button {
                background: linear-gradient(135deg, #667eea, #764ba2); /* Gradient for buttons */
                color: white;
                border-radius: 8px;
                padding: 0.75rem 1.5rem;
                border: none;
                font-size: 16px;
                cursor: pointer;
            }
            .stButton button:hover {
                background: linear-gradient(135deg, #6b46c1, #5a3ea3); /* Hover effect */
            }
            .stSlider .stSlider__track {
                background-color: #3182ce; /* Blue track color */
            }
        </style>
        """

    def get_skill_categories(self):
        return {
            "Technical Skills": [
                "Programming Languages", 
                "Cloud Computing", 
                "Data Analysis", 
                "Machine Learning", 
                "Cybersecurity",
                "Web Development",
                "Database Management"
            ],
            "Soft Skills": [
                "Communication", 
                "Leadership", 
                "Teamwork", 
                "Problem Solving", 
                "Adaptability",
                "Emotional Intelligence",
                "Time Management"
            ],
            "Professional Skills": [
                "Project Management", 
                "Strategic Planning", 
                "Business Analysis", 
                "Digital Marketing", 
                "Financial Literacy",
                "Negotiation",
                "Presentation Skills"
            ]
        }

    def generate_skill_assessment_quiz(self, category, skills):
        """Generate an interactive skill assessment quiz"""
        st.markdown(f"### 📊 {category} Assessment")
        
        assessment_results = {}
        for skill in skills:
            st.markdown(f"#### {skill}")
            
            # Create a slider for skill proficiency
            proficiency = st.slider(
                f"Rate your {skill} proficiency",
                min_value=0, 
                max_value=10, 
                value=5,
                key=f"{category}_{skill}"
            )
            
            # Optional detailed self-assessment
            with st.expander(f"Detailed Assessment for {skill}"):
                expertise_levels = [
                    "Beginner (Limited knowledge)",
                    "Intermediate (Basic working knowledge)",
                    "Advanced (Confident and competent)",
                    "Expert (Advanced problem-solving skills)"
                ]
                selected_level = st.radio(
                    "Select your expertise level", 
                    expertise_levels,
                    key=f"level_{category}_{skill}"
                )
                
                # Additional context input
                context = st.text_area(
                    f"Provide context about your {skill} experience",
                    key=f"context_{category}_{skill}"
                )
            
            assessment_results[skill] = {
                "proficiency": proficiency,
                "level": selected_level,
                "context": context
            }
        
        return assessment_results

    def generate_skill_recommendations(self, assessment_results):
        """Generate AI-powered skill development recommendations"""
        # Prepare input for AI
        input_text = "Provide skill development recommendations based on these assessments: \n"
        for skill, details in assessment_results.items():
            input_text += f"{skill}: Proficiency {details['proficiency']}/10, Level {details['level']}\n"
        
        # Get AI recommendations
        recommendations = self.llm.invoke(input_text)
        return recommendations

    def create_skill_radar_chart(self, assessment_results):
        """Create a radar chart to visualize skills"""
        skills = list(assessment_results.keys())
        proficiencies = [result['proficiency'] for result in assessment_results.values()]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=proficiencies,
            theta=skills,
            fill='toself'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            title='Your Skill Proficiency Radar'
        )
        
        return fig

    def main(self):
        # Set page configuration
        # st.set_page_config(page_title="Career Hub AI - Skill Assessment", page_icon="📊")
        
        # Apply custom CSS
        st.markdown(self.generate_custom_css(), unsafe_allow_html=True)
        
        # Back Button
        col1, col2 = st.columns([8, 1])
        with col2:
            if st.button("🔙 Back", key="back_to_dashboard"):
                st.session_state.page = "home"
        
        # Title
        with col1:
            st.markdown(""" 
            <div class="skill-container">
                <h1 style="text-align: center;">🚀 Comprehensive Skill Assessment</h1>
                <p style="text-align: center; color: #666;">
                    Discover, Evaluate, and Develop Your Professional Skills
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Skill Assessment Process
        st.markdown("## 📋 Assessment Steps")
        
        # Sidebar for guidance
        st.sidebar.header("🧭 Assessment Guide")
        st.sidebar.markdown("""
        ### How to Complete Your Assessment
        1. Rate your skills honestly
        2. Provide context for your expertise
        3. Review recommendations
        4. Create a skill development plan
        """)
        
        # Get skill categories
        skill_categories = self.get_skill_categories()
        
        # Assessment Tabs
        tabs = st.tabs(list(skill_categories.keys()))
        
        # Store all assessment results
        all_assessment_results = {}
        
        # Process each category
        for idx, (category, skills) in enumerate(skill_categories.items()):
            with tabs[idx]:
                # Run skill assessment for this category
                category_results = self.generate_skill_assessment_quiz(category, skills)
                all_assessment_results[category] = category_results
        
        # Generate Recommendations Button
        if st.button("🔍 Generate Skill Insights", type="primary"):
            # Flatten assessment results
            flat_results = {}
            for category, skills in all_assessment_results.items():
                flat_results.update(skills)
            
            # Generate AI Recommendations
            with st.spinner("Generating personalized skill recommendations..."):
                recommendations = self.generate_skill_recommendations(flat_results)
                
                # Display Recommendations
                st.markdown("## 🌟 Personalized Skill Development Recommendations")
                st.markdown(f"""
                <div class="assessment-card">
                    {recommendations}
                </div>
                """, unsafe_allow_html=True)
            
            # Skill Radar Visualization
            st.markdown("## 📊 Skill Proficiency Radar")
            radar_fig = self.create_skill_radar_chart(flat_results)
            st.plotly_chart(radar_fig, use_container_width=True)
            
            # Skill Development Plan
            st.markdown("## 📈 Skill Development Action Plan")
            action_plan_cols = st.columns(3)
            
            skill_development_areas = [
                ("🚀 Immediate Focus", "Skills to develop in the next 3 months"),
                ("🌐 Medium-term Growth", "Skills to enhance in 6-12 months"),
                ("🏆 Long-term Mastery", "Advanced skills for career progression")
            ]
            
            for col, (title, description) in zip(action_plan_cols, skill_development_areas):
                with col:
                    st.markdown(f"""
                    <div class="assessment-card">
                        <h3>{title}</h3>
                        <p>{description}</p>
                    </div>
                    """, unsafe_allow_html=True)

def main():
    skill_assessment = SkillAssessment()
    skill_assessment.main()

if __name__ == "__main__":
    main()
