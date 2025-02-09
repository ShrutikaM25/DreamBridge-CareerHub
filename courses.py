import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

def filter_courses(courses, search_query, category, level):
    filtered_courses = courses.copy()
    
    # Filter by search query
    if search_query:
        filtered_courses = [
            course for course in filtered_courses
            if search_query.lower() in course['title'].lower() or 
               search_query.lower() in course['description'].lower()
        ]
    
    # Filter by category
    if category != "All":
        filtered_courses = [
            course for course in filtered_courses
            if course['category'] == category
        ]
    
    # Filter by level
    if level != "All Levels":
        filtered_courses = [
            course for course in filtered_courses
            if course['level'] == level
        ]
    
    return filtered_courses

def courses_page():
    # Initialize session state for enrollment tracking
    if 'enrolled_courses' not in st.session_state:
        st.session_state.enrolled_courses = set()
    
    # Header Section with Emoji and Styling
    st.markdown("""
        <style>
        .big-font {
            font-size:50px !important;
            font-weight:bold;
            background: linear-gradient(45deg, #1e3799, #0984e3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 10px 0;
        }
        .subheader {
            font-size:25px;
            color: #666;
            margin-bottom: 20px;
        }

        .featured-box {
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .badge {
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            color: white;
            display: inline-block;
            margin: 2px;
        }
        .badge-beginner {
            background-color: #2ecc71;
        }
        .badge-intermediate {
            background-color: #f39c12;
        }
        .badge-advanced {
            background-color: #e74c3c;
        }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<p class="big-font">🎓 SkillUp Hub</p>', unsafe_allow_html=True)
    with col2: 
        if st.button("🔙 Back to Dashboard", key="back_button"):
            st.session_state.page = "home"
    st.markdown('<p class="subheader">Transform your career with cutting-edge courses tailored to industry demands</p>', 
                unsafe_allow_html=True)

    # Skills Assessment Quiz in Sidebar
    st.sidebar.markdown("### 🎯 Skill Assessment")
    if st.sidebar.button("Take Quick Skills Quiz"):
        with st.sidebar:
            st.write("Rate your proficiency (1-5):")
            programming = st.slider("Programming", 1, 5, 3)
            data_analysis = st.slider("Data Analysis", 1, 5, 3)
            design = st.slider("Design", 1, 5, 3)
            
            if st.button("Get Recommendations"):
                avg_score = (programming + data_analysis + design) / 3
                st.info(f"Based on your profile, we recommend starting with {get_level_recommendation(avg_score)} courses.")

    # Main Content
    tab1, tab2, tab3 = st.tabs(["📚 Courses", "🎯 Learning Paths", "📊 Progress Tracker"])

    with tab1:
        # Featured Section
        st.markdown('<div class="featured-box">✨ Featured Course of the Week: Advanced Machine Learning Specialization</div>', 
                   unsafe_allow_html=True)
        
        # Search and Filter Section
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search Courses")
        with col2:
            category = st.selectbox("Category", 
                                  ["All", "Programming", "Data Science", "Design", "Business"])
        with col3:
            level = st.selectbox("Level", 
                               ["All Levels", "Beginner", "Intermediate", "Advanced"])

        # Get and filter courses
        all_courses = get_sample_courses()
        filtered_courses = filter_courses(all_courses, search, category, level)

        if not filtered_courses:
            st.warning("No courses match your filters. Try adjusting your search criteria.")
        
        # Display filtered courses
        for course in filtered_courses:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.subheader(course['title'])
                    st.write(course['description'])
                    st.write(f"👨‍🏫 Instructor: {course['instructor']}")
                    # Display badges
                    level_class = f"badge badge-{course['level'].lower()}"
                    st.markdown(f"""
                        <span class="{level_class}">{course['level']}</span>
                        <span class="badge" style="background-color: #3498db">{course['category']}</span>
                    """, unsafe_allow_html=True)
                with col2:
                    st.write(f"⭐ Rating: {course['rating']}/5.0")
                    st.write(f"⏱️ Duration: {course['duration']}")
                    st.write(f"👥 Enrolled: {course['enrolled']}")
                with col3:
                    st.write(f"💰 Price: ${course['price']}")
                    button_key = f"enroll_{course['title']}"
                    if course['title'] in st.session_state.enrolled_courses:
                        st.success("Enrolled ✓")
                    else:
                        if st.button("Enroll Now", key=button_key):
                            st.session_state.enrolled_courses.add(course['title'])
                            st.success(f"Successfully enrolled in {course['title']}!")
                            st.rerun()
                st.divider()

    with tab2:
        # Learning Paths
        st.header("Curated Learning Paths")
        paths = {
            "Data Scientist 📊": [("Python Basics", "🐍"), ("Data Analysis", "📊"), ("Machine Learning", "🤖")],
            "Full Stack Developer 💻": [("HTML/CSS", "🌐"), ("JavaScript", "📜"), ("React", "⚛"), ("Node.js", "🟢")],
            "UX Designer 🎨": [("Design Principles", "🎨"), ("User Research", "🔍"), ("Prototyping", "🖌")]
        }
        
        selected_path = st.selectbox("Choose your career path", list(paths.keys()))
        
        # Display path steps
        for idx, (course, icon) in enumerate(paths[selected_path], 1):
            st.markdown(f"""
                <div style="padding: 10px; border-radius: 5px; margin: 5px 0;">
                    {idx}. {course} {icon}
                </div>
            """, unsafe_allow_html=True)
            progress = st.progress(0)
            progress.progress(int(idx * 100 / len(paths[selected_path])))

    with tab3:
        # Progress Tracking
        st.header("Your Learning Progress")
        
        # Show enrolled courses progress
        if st.session_state.enrolled_courses:
            progress_data = {
                'Course': list(st.session_state.enrolled_courses),
                'Completion': [30 for _ in st.session_state.enrolled_courses]  # Default 30% progress
            }
        else:
            progress_data = {
                'Course': ['No courses enrolled'],
                'Completion': [0]
            }
            
        df = pd.DataFrame(progress_data)
        
        # Progress visualization
        fig = px.bar(df, x='Course', y='Completion',
                    title='Course Completion Progress',
                    labels={'Completion': 'Completion %'},
                    color='Completion',
                    color_continuous_scale='viridis')
        st.plotly_chart(fig)

        # Study streak
        st.markdown("""
            <div style="padding: 15px; background: linear-gradient(45deg, #2ecc71, #27ae60); 
                        border-radius: 10px; color: white; text-align: center; margin: 20px 0;">
                🔥 Current Study Streak: 7 days
            </div>
        """, unsafe_allow_html=True)
        
        # Weekly study hours
        study_hours = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Hours': [2, 3, 1, 4, 2, 3, 1]
        })
        fig2 = px.line(study_hours, x='Day', y='Hours',
                      title='Weekly Study Hours',
                      markers=True)
        st.plotly_chart(fig2)

def get_level_recommendation(score):
    if score < 2:
        return "Beginner"
    elif score < 4:
        return "Intermediate"
    else:
        return "Advanced"

def get_sample_courses():
    return [
        {
            'title': 'Python for Data Science',
            'description': 'Master Python fundamentals and essential libraries for data analysis',
            'instructor': 'Dr. Sarah Johnson',
            'rating': 4.8,
            'duration': '8 weeks',
            'level': 'Beginner',
            'category': 'Data Science',
            'price': 49.99,
            'enrolled': 1234
        },
        {
            'title': 'Machine Learning Masterclass',
            'description': 'Comprehensive guide to ML algorithms and implementation',
            'instructor': 'Prof. Michael Chen',
            'rating': 4.9,
            'duration': '12 weeks',
            'level': 'Intermediate',
            'category': 'Data Science',
            'price': 79.99,
            'enrolled': 856
        },
        {
            'title': 'Web Development Bootcamp',
            'description': 'Complete guide to modern web development with HTML, CSS, and JavaScript',
            'instructor': 'Jessica Lee',
            'rating': 4.7,
            'duration': '10 weeks',
            'level': 'Beginner',
            'category': 'Programming',
            'price': 59.99,
            'enrolled': 2341
        },
        {
            'title': 'UI/UX Design Fundamentals',
            'description': 'Learn the principles of user interface and experience design',
            'instructor': 'Alex Thompson',
            'rating': 4.8,
            'duration': '6 weeks',
            'level': 'Beginner',
            'category': 'Design',
            'price': 44.99,
            'enrolled': 1567
        },
        {
            'title': 'Advanced React Development',
            'description': 'Master React hooks, context, and advanced patterns',
            'instructor': 'David Wilson',
            'rating': 4.9,
            'duration': '8 weeks',
            'level': 'Advanced',
            'category': 'Programming',
            'price': 89.99,
            'enrolled': 943
        }
    ]

def main():
    courses_page()

if __name__ == "__main__":
    main()