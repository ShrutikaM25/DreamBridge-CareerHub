import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("API_URL")

def fetch_job_data(position=None, company=None, location=None, job_type=None, min_salary=None, max_salary=None):
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()  
        
        filtered_jobs = []  
        
        for job in data:
            if position and position.lower() not in job.get("positionName", "").lower():
                continue
            if company and company.lower() not in job.get("company", "").lower():
                continue
            if location and location.lower() not in job.get("location", "").lower():
                continue
            if job_type and job_type.lower() not in job.get("jobType", "").lower():
                continue
            if min_salary and job.get("salary") and int(job.get("salary").split('-')[0].strip().replace(',', '')) < min_salary:
                continue
            if max_salary and job.get("salary") and int(job.get("salary").split('-')[1].strip().replace(',', '')) > max_salary:
                continue
            
            job_details = {
                "Position": job.get("positionName"),
                "Company": job.get("company"),
                "Location": job.get("location"),
                "Job Type": job.get("jobType"),
                "Salary": job.get("salary"),
                "Rating": job.get("rating"),
                "Reviews": job.get("reviewsCount"),
                "Posted At": job.get("postedAt"),
                "Job URL": job.get("url"),
                "Description": job.get("description"),
            }
            filtered_jobs.append(job_details)  
        
        return filtered_jobs  
    
    else:
        return f"Failed to fetch data. Status code: {response.status_code}" 

# filtered_job_data = fetch_filtered_job_data(position="Software Engineer", company="Dell", location="Remote", job_type="Full-time", min_salary=60000)
# print(filtered_job_data)
