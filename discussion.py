import streamlit as st
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class DiscussionRoom:
    def __init__(self):
        # Initialize AI model
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model_name="mixtral-8x7b-32768", 
            groq_api_key=GROQ_API_KEY, 
            temperature=0.7
        )

    def generate_custom_css(self):
        return """
        <style>
            /* Modern, Professional Design */
            .discussion-container {
                background: linear-gradient(135deg, #1a2a4a 0%, #0d1b2a 100%);
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }
            .ai-response {
                background: linear-gradient(135deg, #222831, #393E46);
                border-left: 4px solid #3182ce;
                padding: 1rem;
                margin: 1rem 0;
                border-radius: 8px;
            }
            .user-query {
                background: linear-gradient(135deg, #232931, #F8A488);
                border-right: 4px solid #4299e1;
                padding: 1rem;
                margin: 1rem 0;
                border-radius: 8px;
                text-align: right;
                display: inline-block; 
                max-width: 80%; 
                word-wrap: break-word;
            }
            .faq-card {
                background: linear-gradient(135deg, #2D2D2D, #3A3A3A);
                border-radius: 10px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
                transition: transform 0.3s ease;
            }
            .faq-card:hover {
                transform: scale(1.02);
            }
            .community-card {
                background: linear-gradient(135deg, #333333, #FFD369);
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }
        </style>
        """

    def generate_dynamic_faqs(self):
        return [
            {
                "question": "How can AI help me in my career development?",
                "answer": "AI can provide personalized career insights, resume optimization, skill gap analysis, and predict potential career paths based on your unique profile and market trends."
            },
            {
                "question": "What makes our Career Hub AI different?",
                "answer": "We combine advanced AI technology with comprehensive career tools, offering personalized roadmaps, real-time market insights, and adaptive learning recommendations."
            },
            {
                "question": "How accurate are the AI-generated career recommendations?",
                "answer": "Our AI uses state-of-the-art language models trained on extensive career and job market data. While highly sophisticated, we recommend using recommendations as guidance and consulting professionals."
            },
            {
                "question": "Can I save and track my career progress?",
                "answer": "Yes! Our platform allows you to save career roadmaps, track skill development, and revisit previous career plans to monitor your growth."
            },
            {
                "question": "Is my data private and secure?",
                "answer": "Absolutely. We use advanced encryption and follow strict data protection protocols to ensure your personal and professional information remains confidential."
            }
        ]

    def ai_query_response(self, query):
        """Generate AI response to user queries"""
        system_prompt = """
        You are an advanced AI career counselor. Provide professional, 
        empathetic, and actionable advice for career-related questions.
        Keep responses concise, informative, and solution-oriented.
        """
        
        full_prompt = f"{system_prompt}\n\nUser Query: {query}"
        response = self.llm.invoke(full_prompt)
        if hasattr(response, "content"):
            return response.content 
        else:
            return "Error: Unexpected response format"

    def generate_community_tips(self):
        """Generate dynamic community career tips"""
        tips = [
            "Network consistently, even when not job hunting.",
            "Invest in continuous learning and skill development.",
            "Personal branding is crucial in today's job market.",
            "Embrace feedback and view it as a growth opportunity.",
            "Always have an updated, ATS-friendly resume.",
            "Learn to articulate your unique value proposition."
        ]
        return random.sample(tips, 3)

    def main(self):
        
        st.markdown(self.generate_custom_css(), unsafe_allow_html=True)
        
        # Back Button
        col1, col2 = st.columns([8, 1])
        with col2:
            if st.button("🔙 Back", key="back_to_dashboard"):
                st.session_state.page = "home"
        
        # Title
        st.markdown("""
        <div class="discussion-container">
            <h1 style="text-align: center;">🤝 Career Hub AI Discussion Room</h1>
            <p style="text-align: center; color: #666;">
                Your AI-powered career companion for personalized guidance and insights
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "💬 Ask AI", 
            "❓ Frequently Asked Questions", 
            "🌟 Community Tips", 
            "🤖 About AI Assistance"
        ])
        
        with tab1:
            st.subheader("🤖 AI Career Counselor")
            user_query = st.text_input("Ask your career-related question:", key="ai_query")
            
            if user_query:
                with st.spinner("Generating response..."):
                    ai_response = self.ai_query_response(user_query)
                    
                st.markdown(f"""
                <div class="user-query">
                    <span style="font-size: 2rem;">👤: </span> {user_query}
                </div>
                <div class="ai-response">
                    <span style="font-size: 2rem;">🤖: </span> {ai_response}
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.subheader("📘 Frequently Asked Questions")
            faqs = self.generate_dynamic_faqs()
            
            for idx, faq in enumerate(faqs, 1):
                with st.expander(f"❓ {faq['question']}"):
                    st.markdown(f"""
                    <div class="faq-card">
                        {faq['answer']}
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab3:
            st.subheader("🌟 Community Career Tips")
            community_tips = self.generate_community_tips()
            
            for tip in community_tips:
                st.markdown(f"""
                <div class="community-card">
                    💡 {tip}
                </div>
                """, unsafe_allow_html=True)
        
        with tab4:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                ### 🚀 Empowering Your Career Journey
                - ✅ **Personalized Career Guidance**  
                - 📊 **Industry Trend Insights**  
                - 🎯 **Career Decision Support**  
                - 📚 **Continuous Learning & Growth**  

                ### ⚙️ How It Works:
                - 🤖 **AI-driven Query Analysis**  
                - 🏆 **Contextual, Professional Responses**  
                - 🎓 **Adaptive Learning Based on Context**  

                ### ⚠️ Limitations:
                - ❗ AI provides **guidance, not absolute decisions**  
                - 🏛️ Must be **complemented with human expertise**  
                - 🔄 Results **may vary based on query complexity**  
                """)

            with col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #3A3D98, #1C1F4A); padding: 20px; border-radius: 12px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);">
                    <h3 style="color: #FFD369; text-align: center;">🔮 Future Scope</h3>
                    <ul style="list-style: none; padding-left: 10px; color: #ffffff;">
                        <li>🎤 <b>AI-powered Mock Interviews</b> - Simulated interviews with real-time feedback</li>
                        <li>📚 <b>Personalized Course Recommendations</b> - AI-curated courses based on skills & interests</li>
                        <li>🗺️ <b>Dynamic Career Roadmaps</b> - AI-driven step-by-step guides for career growth</li>
                        <li>📑 <b>Job Application Optimization</b> - AI-enhanced resumes & ATS tracking</li>
                        <li>📈 <b>Real-time Industry Trend Analysis</b> - Stay ahead with market insights</li>
                        <li>💬 <b>Soft Skills & Communication Training</b> - AI-driven assessments & practice</li>
                        <li>🤝 <b>AI-powered Mentorship Matching</b> - Connect with industry experts</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

def main():
    discussion_room = DiscussionRoom()
    discussion_room.main()

if __name__ == "__main__":
    main()