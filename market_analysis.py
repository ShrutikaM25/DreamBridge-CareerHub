import streamlit as st
import pandas as pd
import requests
from groq import Groq
import plotly.express as px
from datetime import datetime
import json
import random
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def generate_sample_data(company_name, num_jobs=10):
    """
    Generate sample job data for testing and development
    """
    job_titles = [
        "Software Engineer", "Data Scientist", "Product Manager",
        "DevOps Engineer", "UI/UX Designer", "Full Stack Developer",
        "Machine Learning Engineer", "Frontend Developer", "Backend Developer"
    ]
    
    locations = ["Remote", "New York", "San Francisco", "London", "Berlin", "Singapore"]
    
    skills_pool = [
        "Python", "JavaScript", "React", "AWS", "Docker", "Kubernetes",
        "SQL", "Java", "Node.js", "TypeScript", "Git", "MongoDB"
    ]
    
    jobs = []
    for _ in range(num_jobs):
        min_salary = random.randint(80, 150)
        max_salary = min_salary + random.randint(20, 50)
        
        job = {
            "title": random.choice(job_titles),
            "company": company_name,
            "location": random.choice(locations),
            "salary": f"${min_salary},000-${max_salary},000",
            "description": f"Exciting opportunity at {company_name}...",
            "requirements": random.sample(skills_pool, random.randint(3, 6)),
            "posted_date": (datetime.now() - pd.Timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        }
        jobs.append(job)
    
    return jobs

def fetch_real_jobs(company_name):
    """
    Fetch real job data from public APIs
    Note: This is a placeholder - you'll need to replace with actual API endpoints
    """
    try:
        # Example using a public API (replace with your preferred job API)
        api_url = f"https://api.jobs.example.com/search?company={company_name}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            # Fall back to sample data if API fails
            return generate_sample_data(company_name)
            
    except Exception as e:
        st.warning(f"Could not fetch real data: {str(e)}. Using sample data instead.")
        return generate_sample_data(company_name)

def analyze_with_groq(data):
    """
    Analyze job market data using Groq LLM
    """
    prompt = f"""
    Analyze the following job market data and provide detailed insights about the company's market position:
    {json.dumps(data, indent=2)}
    
    Please provide a comprehensive analysis covering:
    1. Overall Market Position
    - Company's hiring trends
    - Job diversity and department distribution
    
    2. Salary Competitiveness
    - Salary range analysis
    - Industry comparison
    - Regional variations
    
    3. Required Skills Analysis
    - Most demanded technical skills
    - Emerging skill requirements
    - Skill combinations
    
    4. Growth Indicators
    - Hiring volume
    - New role creation
    - Department expansion
    
    5. Recommendations
    - Suggested focus areas
    - Competitive positioning
    - Market opportunity gaps
    
    Format the analysis in clear sections with detailed explanations.
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in analysis: {str(e)}"

def create_visualizations(jobs_data):
    """
    Create various visualizations from the job data
    """
    df = pd.DataFrame(jobs_data)
    
    # Extract salary ranges and convert to numeric
    df[['min_salary', 'max_salary']] = df['salary'].str.extract(r'\$(\d+),000-\$(\d+),000').astype(float)
    
    visualizations = {}
    
    # Salary distribution
    fig_salary = px.box(df, y=['min_salary', 'max_salary'], 
                       title="Salary Range Distribution",
                       labels={'value': 'Salary (thousands)', 'variable': 'Range'})
    visualizations['salary_dist'] = fig_salary
    
    # Skills frequency
    skills_list = [skill for job in df['requirements'].tolist() for skill in job]
    skills_freq = pd.Series(skills_list).value_counts()
    fig_skills = px.bar(x=skills_freq.index, y=skills_freq.values,
                       title="Most Required Skills",
                       labels={'x': 'Skills', 'y': 'Frequency'})
    visualizations['skills_freq'] = fig_skills
    
    # Job titles distribution
    title_dist = df['title'].value_counts()
    fig_titles = px.pie(values=title_dist.values, names=title_dist.index,
                       title="Job Titles Distribution")
    visualizations['title_dist'] = fig_titles
    
    # Location distribution
    location_dist = df['location'].value_counts()
    fig_location = px.bar(x=location_dist.index, y=location_dist.values,
                         title="Job Locations Distribution",
                         labels={'x': 'Location', 'y': 'Number of Jobs'})
    visualizations['location_dist'] = fig_location
    
    # Timeline of job postings
    df['posted_date'] = pd.to_datetime(df['posted_date'])
    posting_timeline = df.groupby('posted_date').size().reset_index(name='count')
    fig_timeline = px.line(posting_timeline, x='posted_date', y='count',
                          title="Job Posting Timeline",
                          labels={'posted_date': 'Date', 'count': 'Number of Posts'})
    visualizations['posting_timeline'] = fig_timeline
    
    return visualizations

def main():
    
    st.title("Company Market Position Analysis")
    if st.button("🔙 Back to Dashboard", key="back_button"):
        st.session_state.page = "home"
    
    # Sidebar for inputs
    st.sidebar.header("Analysis Parameters")
    company_name = st.sidebar.text_input("Enter Company Name")
    data_source = st.sidebar.radio("Data Source", ["Sample Data", "Real Data (API)"])
    num_jobs = st.sidebar.slider("Number of Jobs (Sample Data)", 5, 50, 10)
    analyze_button = st.sidebar.button("Analyze")
    
    if analyze_button and company_name:
        try:
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Fetch data
            status_text.text("Fetching job data...")
            progress_bar.progress(25)
            
            if data_source == "Sample Data":
                jobs_data = generate_sample_data(company_name, num_jobs)
                print("Job data: ", jobs_data)
            else:
                jobs_data = fetch_real_jobs(company_name)
            
            # Analyze with Groq
            status_text.text("Analyzing market position...")
            progress_bar.progress(50)
            analysis = analyze_with_groq(jobs_data)
            print("Analysis: ", analysis)
            
            # Create visualizations
            status_text.text("Creating visualizations...")
            progress_bar.progress(75)
            visualizations = create_visualizations(jobs_data)
            
            # Display results
            progress_bar.progress(100)
            status_text.text("Analysis complete!")
            
            # Create two columns for layout
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Display textual analysis
                st.header("Market Analysis")
                st.write(analysis)
                
                # Download option
                st.download_button(
                    label="Download Analysis Report",
                    data=json.dumps({
                        'company': company_name,
                        'analysis': analysis,
                        'raw_data': jobs_data,
                        'generated_at': datetime.now().isoformat()
                    }, indent=2),
                    file_name=f"{company_name}_analysis.json",
                    mime="application/json"
                )
            
            with col2:
                # Display visualizations
                st.header("Visual Insights")
                
                st.subheader("Salary Distribution")
                st.plotly_chart(visualizations['salary_dist'], use_container_width=True)
                
                st.subheader("Required Skills")
                st.plotly_chart(visualizations['skills_freq'], use_container_width=True)
                
                st.subheader("Job Titles")
                st.plotly_chart(visualizations['title_dist'], use_container_width=True)
                
                st.subheader("Job Locations")
                st.plotly_chart(visualizations['location_dist'], use_container_width=True)
                
                st.subheader("Posting Timeline")
                st.plotly_chart(visualizations['posting_timeline'], use_container_width=True)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
if __name__ == "__main__":
    main()