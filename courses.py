import streamlit as st

# List of courses with their YouTube links and thumbnails
courses = [
   
    {
        "title": "Python Programming Full Course",
        "url": "https://www.youtube.com/watch?v=rfscVS0vtbw",
        "thumbnail": "https://img.youtube.com/vi/rfscVS0vtbw/0.jpg"
    },
    {
        "title": "Machine Learning with Python",
        "url": "https://www.youtube.com/watch?v=7eh4d6sabA0",
        "thumbnail": "https://img.youtube.com/vi/7eh4d6sabA0/0.jpg"
    },
    {
        "title": "JavaScript Full Course",
        "url": "https://www.youtube.com/watch?v=hdI2bqOjy3c",
        "thumbnail": "https://img.youtube.com/vi/hdI2bqOjy3c/0.jpg"
    },
    {
        "title": "Web Development Full Course (HTML, CSS, JavaScript)",
        "url": "https://www.youtube.com/watch?v=3JluqTojuME",
        "thumbnail": "https://img.youtube.com/vi/3JluqTojuME/0.jpg"
    },
    {
        "title": "Data Science Full Course",
        "url": "https://www.youtube.com/watch?v=LHBE6Q9XlzI",
        "thumbnail": "https://img.youtube.com/vi/LHBE6Q9XlzI/0.jpg"
    },
    {
        "title": "React JS Full Course",
        "url": "https://www.youtube.com/watch?v=dGcsHMXbSOA",
        "thumbnail": "https://img.youtube.com/vi/dGcsHMXbSOA/0.jpg"
    },
    
    {
        "title": "Building Web Applications with Flask",
        "url": "https://www.youtube.com/watch?v=Z1RJmh_OqeA",
        "thumbnail": "https://img.youtube.com/vi/Z1RJmh_OqeA/0.jpg"
    },
    {
        "title": "Introduction to SQL",
        "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
        "thumbnail": "https://img.youtube.com/vi/HXV3zeQKqGY/0.jpg"
    },
    {
        "title": "Learn C++ Programming",
        "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y",
        "thumbnail": "https://img.youtube.com/vi/vLnPwxZdW4Y/0.jpg"
    }
   
]

# Streamlit UI Configuration
st.set_page_config(page_title="Learn New Skills", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        /* Background Color */
        body {
            background-color: #f4f6f9;
        }
        
        /* Page Title */
        .title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #333333;
        }

        /* Card Container */
        .card {
            background-color: white;
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.3s ease-in-out;
        }
        .card:hover {
            transform: scale(1.05);
        }

        /* Thumbnail Styling */
        .thumbnail {
            border-radius: 10px;
            width: 100%;
            height: auto;
        }

        /* Course Title */
        .course-title {
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
            color: #333333;
        }

            /* Watch Now Button */
    .watch-btn {
        display: inline-block;
        margin-top: 10px;
        padding: 10px 20px;
        background-color: white;
        color: #1f77b4;
        font-size: 16px;
        font-weight: bold;
        text-decoration: none;
        border-radius: 8px;
        border: 2px solid #1f77b4;
        transition: background 0.3s ease-in-out, color 0.3s ease-in-out;
    }
    .watch-btn:hover {
        background-color: #1f77b4;
        color: white;
    }

    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown('<h1 class="title">🎓 Learn New Skills with Top Courses</h1>', unsafe_allow_html=True)

# Create a grid layout with 3 columns
cols = st.columns(3)

# Display courses in a grid format
for i, course in enumerate(courses):
    with cols[i % 3]:
        st.markdown(f"""
            <div class="card">
                <img class="thumbnail" src="{course['thumbnail']}">
                <h4 class="course-title">{course['title']}</h4>
                <a class="watch-btn" href="{course['url']}" target="_blank">▶ Watch Now</a>
            </div>
        """, unsafe_allow_html=True)
