import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import json
import random


# Custom CSS to make the UI more attractive
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #4CAF50;
        color: white;
    }
    .skill-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .insight-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sample skill hierarchies
technical_skills = {
    "Programming Languages": ["Python", "Java", "C++", "JavaScript"],
    "Web Technologies": ["HTML/CSS", "React", "Angular", "Node.js"],
    "Databases": ["MySQL", "MongoDB", "PostgreSQL"],
    "Cloud Platforms": ["AWS", "Azure", "GCP"]
}

soft_skills = {
    "Communication": ["Written", "Verbal", "Presentation"],
    "Leadership": ["Team Management", "Decision Making", "Strategic Planning"],
    "Interpersonal": ["Empathy", "Conflict Resolution", "Collaboration"]
}

professional_skills = {
    "Project Management": ["Agile", "Scrum", "Risk Management"],
    "Business Analysis": ["Requirements Gathering", "Process Modeling", "Documentation"],
    "Quality Assurance": ["Testing", "Quality Control", "Standards Compliance"]
}


def load_questions():
    with open('questions.json') as f:
        return json.load(f)
    
questions_data = load_questions()

def select_random_questions(question_data, skill_type, category, skill):
    key = f"questions_{skill_type}_{category}_{skill}"
    if key not in st.session_state:
        st.session_state[key] = random.sample(
            questions_data.get(skill_type, {}).get(category, {}).get(skill, []),
            min(5, len(questions_data.get(skill_type, {}).get(category, {}).get(skill, [])))
        )
    return st.session_state[key]

def evaluate_response(skill_type, responses, category=None, skill=None):

    if skill_type == "technical_skills":
        score = sum(1 for resp, correct in responses if resp.strip().lower() == correct.strip().lower())
        return (score / len(responses)) * 100 if responses else 0, []
    
    question_list = questions_data.get(skill_type, {}).get(category, {}).get(skill, [])
    expected_keywords = [keyword for q in question_list for keyword in q.get("keywords", [])]


    def keyword_match(response, keywords):
        found_keywords = [keyword for keyword in keywords if keyword.lower() in response.lower()]
        missing_keywords = [keyword for keyword in keywords if keyword.lower() not in response.lower()]
        # print("missing keyword: ", missing_keywords)
        return found_keywords, missing_keywords

    if skill_type in ["soft_skills", "professional_skills"]:
        total_score = 0
        all_missing_keywords = set()

        for response in responses:  
            found, missing = keyword_match(response, expected_keywords)
            # print("missing: ", missing)
            total_score += (len(found) / len(expected_keywords)) * 100 if expected_keywords else 0
            all_missing_keywords.update(missing)

        final_score = total_score / len(responses) if responses else 0
        
        return final_score, list(all_missing_keywords)

    return 0, []
  

def generate_insights(scores):
    insights = []
    print("Score items: ", scores)
    for skill_type, score in scores.items():
        if score >= 80:
            insights.append(f"Strong performance in {skill_type} (Score: {score:.1f}%)")
        elif score >= 60:
            insights.append(f"Good foundation in {skill_type} (Score: {score:.1f}%). Consider advanced training.")
        else:
            insights.append(f"Area for improvement: {skill_type} (Score: {score:.1f}%). Focus on fundamentals.")
    return insights

def generate_recommendations(scores):
    recommendations = []
    for skill_type, score in scores.items():
        if score < 60:
            recommendations.append(f"📚 Take basic {skill_type} courses")
            recommendations.append(f"👥 Join {skill_type} communities")
        elif score < 80:
            recommendations.append(f"🎯 Practice advanced {skill_type} concepts")
            recommendations.append(f"📈 Work on real-world {skill_type} projects")
        else:
            recommendations.append(f"🌟 Consider mentoring others in {skill_type}")
            recommendations.append(f"🎓 Explore cutting-edge {skill_type} topics")
    return recommendations

# Main app
def main():
    col1, col2 = st.columns(2)
    with col1:

        st.title("🎯 Career Skills Assessment Portal")
    with col2:
        if st.button("🔙 Back to Dashboard", key="back_button"):
            st.session_state.page = "home"
    
    # Create tabs for different sections
    tabs = st.tabs(["Technical Skills", "Soft Skills", "Professional Skills", "Results"])
    
    # Initialize session state for storing responses
    if 'responses' not in st.session_state:
        st.session_state.responses = defaultdict(dict)
    if 'scores' not in st.session_state:
        st.session_state.scores = {}
    
    # Technical Skills Tab
    with tabs[0]:
        st.header("Technical Skills Assessment")
        col1, col2 = st.columns(2)
        with col1:
            tech_category = st.selectbox("Select Technology Category", list(technical_skills.keys()))
        with col2:
            if tech_category:
                specific_tech = st.selectbox("Select Specific Skill", technical_skills[tech_category])
        
        if tech_category and specific_tech:
            st.subheader(f"Assessment: {specific_tech}")
            questions = select_random_questions(questions_data, "technical_skills", tech_category, specific_tech)
            responses = []
            
            if questions:
                for i, q in enumerate(questions):
                    answer = st.radio(f"Q{i+1}: {q['question']}", q['options'],index=None, key=f"{specific_tech}_{i}")
                    responses.append((answer, q['answer']))
                    if f"show_answer_{specific_tech}_{i}" in st.session_state:

                        if answer == q['answer']:
                            st.info(f"✅ Correct Answer: {q['answer']}")
                        else:
                            st.error(f"❌ Incorrect Answer: {answer}")
                            st.info(f"✅ Correct Answer: {q['answer']}")

            else:
                st.warning(f"No questions available for {specific_tech}.")

            if st.button("Submit Assessment"):
                score, missing_keywords = evaluate_response("technical_skills", responses)
                st.session_state.scores[f"Technical: {specific_tech}"] = score
                for i in range(len(questions)):
                    st.session_state[f"show_answer_{specific_tech}_{i}"] = True
                st.success(f"Assessment submitted! Your Score: {score:.1f}%")
            
    
    # Soft Skills Tab
    with tabs[1]:
        st.header("Soft Skills Assessment")
        soft_category = st.selectbox("Select Soft Skill Category", list(soft_skills.keys()))
        if soft_category:
            specific_soft = st.selectbox("Select Specific Skill", soft_skills[soft_category])
            
            if specific_soft:
                st.subheader(f"Assessment: {specific_soft}")
                questions = select_random_questions(questions_data, "soft_skills",soft_category, specific_soft)
                responses = []
                
                if questions:
                    for i, q in enumerate(questions):
                        st.write(f"Q{i+1}: {q['question']}")
                        answer = st.text_area(f"Your response for Q{i+1}", key=f"soft_{specific_soft}_{i}")
                        responses.append(answer)
                    
                    if st.button("Submit Soft Skills Assessment", key="soft_submit"):
                        expected_keywords= questions_data.get(soft_category, {})
                        print("Expected keywords: ", expected_keywords)
                        score, missing_keywords = evaluate_response("soft_skills", responses, soft_category, specific_soft)
                        print("Score: ", score)

                        st.session_state.scores[f"Soft: {specific_soft}"] = score
                        st.success(f"Assessment submitted! Evaluation score: {score:.1f}%")

                        if missing_keywords:  
                            st.warning(f"Consider including these keywords for a better score: {', '.join(missing_keywords)}")
                        else:
                            st.info("Great job! You've included all relevant keywords.")
                else:
                    st.warning(f"No questions available for {specific_tech}.")
    
    # Professional Skills Tab
    with tabs[2]:
        st.header("Professional Skills Assessment")
        prof_category = st.selectbox("Select Professional Skill Category", list(professional_skills.keys()))
        if prof_category:
            specific_prof = st.selectbox("Select Specific Skill", professional_skills[prof_category])
            
            if specific_prof:
                st.subheader(f"Assessment: {specific_prof}")
                questions = select_random_questions(questions_data, "professional_skills", prof_category, specific_prof)
                responses = []
                if questions:
                    for i, q in enumerate(questions):
                        st.write(f"Q{i+1}: {q['question']}")
                        answer = st.text_area(f"Your response for Q{i+1}", key=f"prof_{specific_prof}_{i}")
                        responses.append(answer)
                    
                    if st.button("Submit Professional Skills Assessment", key="prof_submit"):
                        score, missing_keywords = evaluate_response("professional_skills", responses, prof_category, specific_prof)
                        st.session_state.scores[f"Professional: {specific_prof}"] = score
                        st.success(f"Assessment submitted! Evaluation score: {score:.1f}%")
                        if missing_keywords:  
                            st.warning(f"Consider including these keywords for a better score: {', '.join(missing_keywords)}")
                        else:
                            st.info("Great job! You've included all relevant keywords.")
            else:
                st.warning(f"No questions available for {specific_tech}.")
    
    # Results Tab
    with tabs[3]:
        st.header("Assessment Results & Insights")
        
        if st.session_state.scores:
            # Display scores in an attractive way
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📊 Score Overview")
                fig = go.Figure()
                
                categories = list(st.session_state.scores.keys())
                scores = list(st.session_state.scores.values())
                
                fig.add_trace(go.Bar(
                    x=categories,
                    y=scores,
                    marker_color=['#1f77b4' if 'Technical' in cat else '#2ca02c' if 'Soft' in cat else '#ff7f0e' 
                                for cat in categories]
                ))
                
                fig.update_layout(
                    title="Skills Assessment Results",
                    xaxis_title="Skill Categories",
                    yaxis_title="Score (%)",
                    template="plotly_white",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🎯 Skill Distribution")
                fig = px.pie(
                    values=scores,
                    names=categories,
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            st.subheader("🔍 Key Insights")
            insights = generate_insights(st.session_state.scores)
            for insight in insights:
                st.info(insight)
            
            # Recommendations
            st.subheader("💡 Recommendations")
            recommendations = generate_recommendations(st.session_state.scores)
            cols = st.columns(2)
            for i, rec in enumerate(recommendations):
                with cols[i % 2]:
                    st.success(rec)
            
            # Radar Chart
            st.subheader("📈 Skills Radar")
            categories = list(st.session_state.scores.keys())
            scores = list(st.session_state.scores.values())
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]],
                theta=categories + [categories[0]],
                fill='toself',
                line_color='#1f77b4'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()