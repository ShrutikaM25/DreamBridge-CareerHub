import streamlit as st
import requests
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from new import fetch_job_data 

# Load API keys
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Market Analysis Agent
def market_analysis_agent():
    llm = ChatGroq(model_name="mixtral-8x7b-32768", api_key=GROQ_API_KEY, temperature=0.5)

    prompt = PromptTemplate(
        input_variables=["data"],
        template=(
            "You are an expert job market analyst. Based on the provided real-time job market data, generate a report covering:\n"
            "- **High-Demand Job Roles:** Identify top job positions based on frequency and salary trends.\n"
            "- **Salary Trends:** Provide insights on salary distributions, average salaries, and variations by location and company.\n"
            "- **Emerging Skills:** Detect trending skills and technologies sought by employers.\n"
            "- **Company Insights:** Highlight active hiring companies and compare their offerings.\n"
            "- **Job Type Analysis:** Break down job types (full-time, part-time, contract, internship) and their market share.\n\n"
            "Use bullet points for key insights. If applicable, mention any significant hiring shifts.\n\n"
            "**Data Provided:** {data}"
        )
    )

    return LLMChain(llm=llm, prompt=prompt)

def filter_jobs(df, position, company, location, salary_min, salary_max):
    filtered_df = df.copy()

    if position:
        filtered_df = filtered_df[filtered_df["Position"].str.contains(position, case=False, na=False)]
    if company:
        filtered_df = filtered_df[filtered_df["Company"].str.contains(company, case=False, na=False)]
    if location:
        filtered_df = filtered_df[filtered_df["Location"].str.contains(location, case=False, na=False)]
    if salary_min is not None and salary_max is not None:
        filtered_df = filtered_df[(filtered_df["Salary"] >= salary_min) & (filtered_df["Salary"] <= salary_max)]

    return filtered_df

def analyze_market():
    job_data = fetch_job_data()  # Fetch job data
    if isinstance(job_data, str) and job_data.startswith("Failed"):
        return job_data  # Return error message if data fetch fails

    formatted_jobs = [
        {"title": job["Position"], "salary": job["Salary"], "location": job["Location"], "type": job["Job Type"]}
        for job in job_data
    ]

    chain = market_analysis_agent()
    insights = chain.run({"data": formatted_jobs})
    
    return insights, pd.DataFrame(formatted_jobs)  # Return insights & DataFrame for visualization

# Streamlit UI
def main():
    st.title("📊 Job Market Analysis Dashboard")
    col1, col2 = st.columns([5, 1]) 
    with col2:
        if st.button("🔙 Back to Dashboard", key="back_to_dashboard"):
            st.session_state.page = "home"
    st.markdown("Gain insights into the current job market trends with AI-powered analysis and visualizations.")

    # Run the market analysis when button is pressed
    if st.button("🔍 Analyze Market Data"):
        with st.spinner("Fetching and analyzing job data..."):
            analysis_results, df = analyze_market()

            # Show textual analysis
            if isinstance(analysis_results, str) and analysis_results.startswith("Failed"):
                st.error(analysis_results)  # Show error if fetching failed
            else:
                st.subheader("📌 Market Analysis Insights:")
                st.write(analysis_results)  # Display the AI-generated market insights

                # Data Cleaning: Convert salary column to numeric
                df["salary"] = pd.to_numeric(df["salary"], errors='coerce')

                # --- 📈 Salary Distribution Chart ---
                st.subheader("💰 Salary Distribution")
                fig_salary = px.histogram(df, x="salary", nbins=30, title="Salary Distribution", labels={"salary": "Salary ($)"})
                st.plotly_chart(fig_salary, use_container_width=True)

                # --- 📊 Job Type Distribution ---
                st.subheader("📌 Job Type Distribution")
                filtered_df = df[df["type"].apply(lambda x: bool(x) and x != [])]
                if not filtered_df.empty:
                    job_type_counts = filtered_df["type"].explode().value_counts()  # 'explode' to flatten the lists
                    fig_job_type = px.pie(names=job_type_counts.index, values=job_type_counts.values, title="Job Type Breakdown")
                    st.plotly_chart(fig_job_type, use_container_width=True)
                else:
                    st.warning("No valid job type data available.")

                # --- 🌎 Location-Based Demand ---
                st.subheader("🌍 Job Demand by Location")
                location_counts = df["location"].value_counts().reset_index()
                location_counts.columns = ["Location", "Job Count"]
                fig_location = px.bar(location_counts, x="Location", y="Job Count", title="Top Hiring Locations")
                st.plotly_chart(fig_location, use_container_width=True)

if __name__ == '__main__':
    main()
