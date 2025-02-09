import streamlit as st
import random


# Sample interview questions and ideal answers for different roles
INTERVIEW_DATA = {
    "Software Engineer": {
        "technical": [
            {
                "question": "Can you explain the difference between procedural and object-oriented programming?",
                "ideal_answer": "Procedural programming focuses on procedures or functions that operate on data, while object-oriented programming organizes code into objects that contain both data and methods. OOP promotes concepts like inheritance, encapsulation, and polymorphism.",
                "keywords": ["inheritance", "encapsulation", "polymorphism", "objects", "methods", "functions"]
            },
            {
                "question": "How do you handle error conditions in your code?",
                "ideal_answer": "I use try-catch blocks for exception handling, implement proper error logging, and ensure graceful degradation. I also believe in failing fast and providing meaningful error messages.",
                "keywords": ["try-catch", "exception", "logging", "error handling", "debugging"]
            }
        ],
        "behavioral": [
            {
                "question": "Tell me about a challenging project you worked on and how you overcame obstacles.",
                "ideal_answer": "Focus on specific examples, demonstrate problem-solving skills, team collaboration, and successful outcome achievement.",
                "keywords": ["challenge", "solution", "team", "collaboration", "outcome", "success"]
            }
        ]
    },
    "Data Scientist": {
        "technical": [
            {
                "question": "Explain the difference between supervised and unsupervised learning.",
                "ideal_answer": "Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data. Examples include classification vs clustering.",
                "keywords": ["labeled", "unlabeled", "classification", "clustering", "patterns", "training"]
            }
        ],
        "behavioral": [
            {
                "question": "How do you explain complex technical concepts to non-technical stakeholders?",
                "ideal_answer": "I use analogies, visual aids, and simple language. I focus on business impact and practical applications rather than technical details.",
                "keywords": ["analogies", "visual", "simple", "stakeholders", "communication"]
            }
        ]
    }
}

def calculate_confidence_score(answer, keywords):
    """Calculate a confidence score based on keyword matches"""
    score = 0
    answer_lower = answer.lower()
    for keyword in keywords:
        if keyword.lower() in answer_lower:
            score += 1
    return min((score / len(keywords)) * 100, 100)

def generate_feedback(answer, ideal_answer, confidence_score):
    """Generate feedback based on the answer and confidence score"""
    feedback = []
    
    if confidence_score >= 80:
        feedback.append("Excellent response! You covered the key points effectively.")
    elif confidence_score >= 60:
        feedback.append("Good answer, but there's room for improvement.")
    else:
        feedback.append("Consider incorporating more specific details in your response.")
    
    if confidence_score < 100:
        feedback.append(f"\nConsider including these points:\n{ideal_answer}")
    
    return "\n".join(feedback)

def main():
    st.title("AI Mock Interview Simulator 🤖") 

    if st.button("🔙 Back to Dashboard", key="back_button"):
        st.session_state.page = "home"
    
    # Sidebar for interview settings
    st.sidebar.title("Interview Settings")
    role = st.sidebar.selectbox("Select Role", list(INTERVIEW_DATA.keys()))
    interview_type = st.sidebar.selectbox("Interview Type", ["Technical", "Behavioral", "Mixed"])

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    if 'feedback_history' not in st.session_state:
        st.session_state.feedback_history = []
    if 'confidence_scores' not in st.session_state:
        st.session_state.confidence_scores = []
    
    # Main interview interface
    if not st.session_state.interview_started:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("""
            ### Welcome to Your AI Interview Preparation! 📝
            
            This platform will help you:
            - Practice role-specific interview questions
            - Receive real-time feedback on your answers
            - Track your progress and improvement
            - Build confidence for your real interview
            
            Ready to begin? Click 'Start Interview' to proceed!
            """)

        # if st.button("🔙 Back to Dashboard", key="back_button"):
        #     st.session_state.page = "home"
        
        with col2:
            st.image("https://media.giphy.com/media/robot-ai-gif/giphy.gif", use_column_width=True)
        
        if st.button("Start Interview", type="primary"):
            st.session_state.interview_started = True
            st.rerun()
        
        # with col3:
        #     if st.button("🔙 Back to Dashboard", key="back_button"):
        #         st.session_state.page = "home"
    
    else:
        # Interview in progress
        questions = INTERVIEW_DATA[role]["technical" if interview_type == "Technical" 
                                     else "behavioral" if interview_type == "Behavioral"
                                     else random.choice(["technical", "behavioral"])]
        
        if st.session_state.current_question < len(questions):
            current_q = questions[st.session_state.current_question]
            
            # Display progress
            progress = st.progress((st.session_state.current_question) / len(questions))
            st.write(f"Question {st.session_state.current_question + 1} of {len(questions)}")
            
            # Display question with some animation
            st.markdown(f"### Q: {current_q['question']}")
            
            user_answer = st.text_area("Your Answer:", height=150, key=f"answer_{st.session_state.current_question}")
            
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Submit Answer"):
                    if user_answer:
                        # Calculate confidence score
                        st.session_state.latest_feedback = ""
                        st.session_state.latest_confidence_score = 0
                        
                        confidence_score = calculate_confidence_score(user_answer, current_q['keywords'])
                        st.session_state.confidence_scores.append(confidence_score)
                        
                        # Generate and store feedback
                        feedback = generate_feedback(user_answer, current_q['ideal_answer'], confidence_score)
                        st.session_state.feedback_history.append({
                            'question': current_q['question'],
                            'answer': user_answer,
                            'feedback': feedback,
                            'confidence_score': confidence_score
                        })
                         # Store the latest feedback in session state
                        st.session_state.latest_feedback = feedback
                        st.session_state.latest_confidence_score = confidence_score
                        
            if "latest_feedback" in st.session_state and st.session_state.latest_feedback:
                st.markdown("---") 

                # Display Feedback (Full Width)
                st.markdown("## Feedback:")
                st.write(st.session_state.latest_feedback)


                # Display Confidence Score (Full Width)
                st.markdown(f"## Confidence Score: {st.session_state.latest_confidence_score:.1f}%")
                st.progress(st.session_state.latest_confidence_score / 100)


                if st.session_state.current_question <= len(questions) - 1:
                    with col2:
                        if st.button("Next Question"):
                                st.session_state.current_question += 1
                                st.rerun()

            
        
        else:
            st.success("🎉 Interview Completed!")
            
            avg_confidence = sum(st.session_state.confidence_scores) / len(st.session_state.confidence_scores) if st.session_state.confidence_scores else 0
            st.markdown(f"### Overall Performance: {avg_confidence:.1f}%")
            st.progress(avg_confidence/100)
            
            # Display detailed feedback for each question
            st.markdown("### Detailed Feedback")
            for idx, feedback in enumerate(st.session_state.feedback_history, 1):
                with st.expander(f"Question {idx}: {feedback['question']}"):
                    st.write("Your Answer:", feedback['answer'])
                    st.write("Feedback:", feedback['feedback'])
                    st.write(f"Confidence Score: {feedback['confidence_score']:.1f}%")
            
            # Option to restart

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Start New Interview"):
                    st.session_state.current_question = 0
                    st.session_state.latest_feedback = ""
                    st.session_state.latest_confidence_score = 0
                    st.session_state.interview_started = False
                    st.session_state.feedback_history = []
                    st.session_state.confidence_scores = []

                    st.rerun()
            # with col2:
            #     if st.button("🔙 Back to Dashboard", key="back_button"):
            #         st.session_state.page = "home"

if __name__ == "__main__":
    main()