# <div align="center">**NLP Resume Evaluation**</div>
---
<div align="center">


Effortlessly automate your hiring workflow with this advanced NLP-powered system:

- **Automatic CV Extraction & Structuring:** Instantly parses and organizes resumes into key sections using AI.
- **Semantic Matching:** Compares candidate profiles to job descriptions with custom Word2Vec embeddings for deep semantic analysis.
- **Smart Scoring & Ranking:** Calculates similarity scores and ranks applicants for optimal selection.
- **Interactive Visualization:** Explore results in a modern Flask web app, seamlessly orchestrated via n8n workflows.

</div>

---
## <div align="center">Technologies Used</div>
<div align="center">
    <img src="https://i.ibb.co/5wcQ01H/image.png" alt="Python" width="700" style="border-radius: 20px;">
</div>

## 🛠️ Minimal Tech Stack Overview

- **Python**: Main programming language for backend logic and data processing.
- **Flask**: Lightweight web framework for serving APIs and visualizing results.
- **n8n**: Workflow automation tool for orchestrating email processing and integration.
- **MongoDB**: NoSQL database for storing structured CVs and scores.
- **Word2Vec**: Custom-trained model for generating text embeddings.
- **Docker**: Containerization for easy deployment and reproducibility.
- **Gmail API**: For automated email retrieval and monitoring.


<p align="center">
  <a href="#-key-features">Key Features</a> •
  <a href="#-technologies-used">Technologies</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-acknowledgements">Acknowledgements</a>
</p>



---

## 🎯 Key Features

*   **Automated Email Classification**: Automatically classifies incoming emails into three categories: `High Priority`, `Low Priority`, and `Job Application` using a supervised machine learning model.
*   **CV Scoring System**: Extracts resumes from `Job Application` emails, analyzes their content, and scores them against a given job description using cosine similarity.
*   **n8n Workflow Orchestration**: The entire process is orchestrated through a powerful and flexible n8n workflow, connecting various services and APIs seamlessly.
*   **NLP-Powered Analysis**: Uses a custom-deployed Word2Vec model to generate vector representations of text, enabling deep semantic understanding of resumes and job descriptions.
*   **Web-Based Visualization**: A Flask-based web application displays the ranked list of candidates, making it easy for recruiters to identify the most suitable applicants.
*   **Modular and Scalable**: The architecture is designed to be modular, allowing for easy integration of new models or services.

---

## 🏗️ System Architecture

The system is composed of two main parts: an **n8n workflow** for process automation and a **Flask web application** for model serving and results visualization.

<p align="center">
  <img src="https://i.ibb.co/4nzgGq7Z/image.png" alt="High-Level Architecture" width="700" style="border-radius: 20px;">
  <br>
  <em>High-Level System Architecture</em>
</p>

The workflow is triggered by a new email, classifies it, and if it's a job application, calls the Flask API to score the resume and stores the result in MongoDB. The frontend then fetches the ranked list of candidates.

---

## ⚙️ How It Works

The core of this project is the automated CV evaluation process, detailed in **Chapter 6** of the project report. Here’s a step-by-step breakdown:

### 1. Email Classification and CV Extraction

The n8n workflow begins when a new email arrives.
1.  **Trigger**: A `Gmail Trigger` node detects a new email.
2.  **Classification**: An `HTTP Request` node sends the email body to a deployed classification model.
3.  **Routing**: A `Switch` node routes the workflow based on the classification (`High Priority`, `Low Priority`, or `Job Application`).


### 2. CV Sectioning and Vectorization

For job applications, the system performs the following steps:
1.  **File Extraction**: The attached CV (PDF) is extracted and its raw text is obtained using the `Extract from File` node.
2.  **AI-Powered Sectioning**: An `AI Agent` (using a Large Language Model) structures the raw text into standardized JSON sections: `professional_summary`, `work_experience`, `education`, `skills`, and `others`.

3.  **Vectorization**: Each section of the CV and the job description is sent to a deployed API endpoint, which uses a custom Word2Vec model to return a 100-dimension numerical vector.

### 3. Cosine Similarity and Scoring

The relevance of a candidate is determined by comparing their CV to the job description.
1.  **Similarity Calculation**: The system calculates the **cosine similarity** between the vector of each CV section and the corresponding section of the job description. This measures the semantic similarity, not just keyword matching.
<p align="center">
  <img src="https://i.imgur.com/bW7tV8k.png" alt="Cosine Similarity" width="500">
  <br>
  <em>Cosine similarity measures the angle between two vectors.</em>
</p>

2.  **Weighted Scoring**: Each section's similarity score is multiplied by a predefined weight (e.g., `work_experience` and `skills` are weighted higher).
<p align="center">
  <img src="https://i.imgur.com/t8fG3pS.png" alt="Section Weights" width="400">
  <br>
  <em>Empirically determined weights for each section.</em>
</p>

3.  **Final Score**: The weighted scores are summed up to produce a final, global score for the candidate.

### 4. Data Storage and Visualization

1.  **Storage**: The structured CV, along with its detailed and final scores, is saved as a document in a MongoDB database.
2.  **Display**: A user can navigate to the Flask application's `/get_resume` endpoint, which retrieves all candidates from MongoDB, sorts them by their final score in descending order, and displays them on a clean, user-friendly web page.

<p align="center">
  <img src="https://i.imgur.com/L4e9o2f.png" alt="Candidate Leaderboard" width="700">
  <br>
  <em>Final web application showing ranked candidates.</em>
</p>

---

## 🚀 Installation

To set up this project locally, you will need Python, Docker, and access to an n8n instance.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Set up the Python environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file and add your MongoDB connection string and other necessary credentials.
    ```
    MONGO_URI="your_mongodb_connection_string"
    ```

4.  **Run the application:**
    You can run the Flask app directly or use the provided Dockerfile.
    ```bash
    # To run with Flask
    flask run

    # To build and run with Docker
    docker build -t resume-scorer .
    docker run -p 5000:5000 resume-scorer
    ```

---

## 📖 Usage

1.  **Deploy the Models**: Ensure your classification and vectorization models are deployed (e.g., on Hugging Face Spaces) and that the API endpoints are accessible.
2.  **Configure n8n**: Import the workflow JSON file into your n8n instance. Update the `HTTP Request` nodes with your deployed model URLs and the Flask application's endpoint.
3.  **Start the Process**: Send an email with a CV attached to the monitored Gmail account.
4.  **View Results**: Open your browser and navigate to `http://localhost:5000/get_resume` to see the ranked list of candidates.

---

## 🙏 Acknowledgements

This project was submitted in partial fulfillment of the requirements for the Bachelor's Degree in Data Science and Decision Informatics at the Faculty of Sciences and Techniques of Mohammedia.

*   **Project Supervisor**: Prof. Asmaa ABASSI
*   A special thanks to the entire jury and everyone who provided support and guidance throughout this project.

---

## 📄 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute with attribution.

<div align="center">
  <h4>Happy Automating!</h4>
</div>

<div align="center">
  <h3>⭐ If you found this project useful, please give it a star!</h3>
  <a href="https://github.com/your-username/your-repo-name">
    <img src="https://img.shields.io/github/stars/your-username/your-repo-name?style=social" alt="GitHub stars">
  </a>
</div>


