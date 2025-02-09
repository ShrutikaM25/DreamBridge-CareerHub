import streamlit as st
st.set_page_config(page_title="Career Hub AI", layout="wide")

import ats_tracker
import career_roadmap
import market_analysis
import discussion
import courses
import skill_assessment
import mock_interview
import top_educators
import scenario_based_evaluation

# Custom Styles
st.markdown("""
    <style>
        body {
            background-color: #1A1F25;
            font-family: 'Segoe UI', sans-serif;
        }
        
        .main-title {
            text-align: center;
            font-size: 52px;
            font-weight: 800;
            background: linear-gradient(120deg, #6E45E2, #88D3CE, #6E45E2);
            background-size: 200% auto;
            color: transparent;
            background-clip: text;
            -webkit-background-clip: text;
            animation: gradient 3s ease infinite;
            margin: 40px 0 20px;
        }
            
         /* Animations */
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .sub-title {
            text-align: center;
            font-size: 22px;
            color: #A0AEC0;
            margin-bottom: 40px;
        }
        
        .feature-card {
            background: #2D3748;
            padding: 20px;
            height: 350px;
            margin: 10px 0;
            text-align: center;
            color: white;
            border-radius: 16px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .feature-card:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateZ(20px) rotateZ(10deg);
            box-shadow: 0 16px 64px rgba(110, 69, 226, 0.3);
        }
        
        .feature-icon {
            font-size: 60px;
            margin-bottom: 20px;
        }
        
        .feature-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .feature-description {
            font-size: 16px;
            margin-bottom: 20px;
        }
        
        .footer {
            text-align: center;
            font-size: 14px;
            color: #A0AEC0;
            padding: 20px;
            margin-top: 40px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Navigation State
if "page" not in st.session_state:
    st.session_state.page = "home"
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">DreamBridge AI</h1>
        <p class="sub-title">Elevate Your Career Journey with AI-Powered Insights</p>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown("<h2 class='sub-title'>Discover Your Career Tools</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    card_info = [
        ("🚀", "NextGen Career Suite", "Advanced resume optimization using AI to maximize your application success rate. Get detailed insights and recommendations.", "Optimize Resume", "ats_tracker"),
        ("🧭", "Career Roadmap", "Personalized career progression planning with AI insights. Map your journey and identify growth opportunities.", "Plan Your Path", "career_roadmap"),
        ("📊", "Market Analysis", "Real-time industry insights and salary benchmarks to help you make informed career decisions.", "Explore Trends", "market_analysis"),
        ("💬", "AI Career Discussion", "Engage in AI-driven career discussions, get expert opinions, and explore different career perspectives.", "Start Discussion", "discussion"),
        ("📚", "Courses", "Access curated courses to upskill and stay competitive in your career. Learn at your own pace.", "Explore Courses", "courses"),
        ("🧠", "Skill Assessment", "Evaluate your skills with AI-powered assessments and track your growth over time.", "Assess Skills", "skill_assessment"),
        ("🎤", "AI-Powered Mock Interview", "Practice for your next interview with AI-generated questions tailored to your desired role.", "Start Mock Interview", "mock_interview"),
        ("🏆", "Top Educators", "Find top mentors and educators based on AI-powered search and recommendation system.", "Find Mentors", "top_educators"),
        ("🔍", "Job Role Prediction", "Get AI-based predictions for suitable job roles based on your skills.", "Predict Job Role", "scenario_based_evaluation"),
    ]
    
    # Fill columns with cards
    for idx, (icon, title, desc, button_text, page_link) in enumerate(card_info):
        with [col1, col2, col3, col4][idx % 4]:  # Distribute cards into columns
            st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-description">{desc}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Create the button to navigate to respective pages
            if st.button(button_text, key=page_link):
                st.session_state.page = page_link

# Redirecting to specific pages
elif st.session_state.page == "ats_tracker":
    ats_tracker.main()
elif st.session_state.page == "career_roadmap":
    career_roadmap.main()
elif st.session_state.page == "market_analysis":
    market_analysis.main()
elif st.session_state.page == "discussion":
    discussion.main()
elif st.session_state.page == "courses":
    courses.main()  
elif st.session_state.page == "skill_assessment":
    skill_assessment.main()
elif st.session_state.page == "mock_interview":
    mock_interview.main()
elif st.session_state.page == "scenario_based_evaluation":
    scenario_based_evaluation.main()
elif st.session_state.page == "top_educators":
    top_educators.main()

# Footer
st.markdown("""
    <div class="footer" style="margin-bottom: 8px">
        <div>💼 Powered by Advanced AI Technology</div>
        <div style="margin-top: 8px;">© 2025 Career Hub AI - Empowering Career Growth</div>
    </div>
""", unsafe_allow_html=True)
