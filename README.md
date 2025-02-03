# Career Roadmap Generator

## Overview
The **Career Roadmap Generator** is a Streamlit-based web application that helps users generate a personalized career roadmap based on their skills, interests, education level, and preferred industries. It leverages LangChain and Groq's LLM to provide detailed recommendations, including career paths, required skills, job roles, and suggested courses with links.

## Features
- 🚀 **User-Friendly UI** built with Streamlit
- 🤖 **AI-Powered Career Recommendations** using LangChain and Groq
- 📚 **Recommended Courses** with clickable links
- 🎯 **Interactive Input Fields** for skills, interests, education level, and industry preferences

## Tech Stack
- **Python** (Backend Logic)
- **Streamlit** (UI Framework)
- **LangChain & Groq** (LLM Integration)
- **Dotenv** (Environment Variable Management)

## Setup Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/ShrutikaM25/DreamBridge-CareerHub.git
cd your-repo-name
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
#### For Windows
```sh
python -m venv venv
venv\Scripts\activate
```
#### For macOS/Linux
```sh
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the root directory and add your **GROQ_API_KEY**:
```sh
GROQ_API_KEY=your-api-key-here
GOOGLE_API_KEY=your-api-key-here
RAPIDAPI_KEY=your-api-key-here
```

### 5️⃣ Run the Streamlit App
```sh
streamlit run app.py
```

## Usage
1. Enter your current skills and interests.
2. Select your **Education Level** and **Preferred Industries** from dropdowns.
3. Click **Generate Roadmap** to receive personalized career recommendations.
4. View suggested **career paths, skills to develop, job roles, and certification courses** with links.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue.

## License
This project is licensed under the **MIT License**.

---
🔗 **Connect with us:** [LinkedIn](https://www.linkedin.com/) | [GitHub](https://github.com/)

