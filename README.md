# <div align="center">**Resume Evaluation using Natural Language Processing (NLP)**</div>
<div align="center">
    <img src="https://i.ibb.co/Kp4BQ4hn/image.png" alt="Python" width="300" style="border-radius: 20px;">
</div>
<p align="center">
  <a href="#live-demo">Live Demo</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#technologies-used">Technologies Used</a> •
  <a href="#system-architecture">System Architecture</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-license">License</a>
</p>

---
<div align="center">


## Overview

</div>

Effortlessly automate your hiring workflow with this advanced NLP-powered system:

- **Automatic CV Extraction & Structuring:** Instantly parses and organizes resumes into key sections using AI.
- **Semantic Matching:** Compares candidate profiles to job descriptions with custom Word2Vec embeddings for deep semantic analysis.
- **Smart Scoring & Ranking:** Calculates similarity scores and ranks applicants for optimal selection.
- **Interactive Visualization:** Explore results in a modern Flask web app, seamlessly orchestrated via n8n workflows.


---

## Live Demo

Deployed on **Hugging Face Spaces**:  
**https://huggingface.co/spaces/moghit/resume-evaluation**

> _Note: the Space may need a little time to start if it’s been sleeping._

<a id="technologies-used"></a>
## <div align="center">Technologies Used</div>
<div align="center">
    <img src="https://i.ibb.co/5wcQ01H/image.png" alt="Python" width="700" style="border-radius: 20px;">
</div>


- **Python**: Main programming language for backend logic and data processing.
- **Flask**: Lightweight web framework for serving APIs and visualizing results.
- **n8n**: Workflow automation tool for orchestrating email processing and integration.
- **MongoDB**: NoSQL database for storing structured CVs and scores.
- **Word2Vec**: Custom-trained model for generating text embeddings.
- **Docker**: Containerization for easy deployment and reproducibility.
- **Gmail API**: For automated email retrieval and monitoring.
- **AWS EC2**: Cloud infrastructure used to host and run the entire n8n workflow.  







---

## Key Features

*   **Automated Email Classification**: Automatically classifies incoming emails into three categories: `High Priority`, `Low Priority`, and `Job Application` using a supervised machine learning model.
*   **CV Scoring System**: Extracts resumes from `Job Application` emails, analyzes their content, and scores them against a given job description using cosine similarity.
*   **n8n Workflow Orchestration**: The entire process is orchestrated through a powerful and flexible n8n workflow, connecting various services and APIs seamlessly.
*   **NLP-Powered Analysis**: Uses a custom-deployed Word2Vec model to generate vector representations of text, enabling deep semantic understanding of resumes and job descriptions.
*   **Web-Based Visualization**: A Flask-based web application displays the ranked list of candidates, making it easy for recruiters to identify the most suitable applicants.


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
<a id="how-it-works"></a>

## ⚙️ How It Works

The core of this project is the automated CV evaluation process, detailed in **Chapter 6** of the project report.
Refer to Chapter 6 in the project report [here](https://drive.google.com/file/d/1zczUyl51G2qE0vfhcx6JZmcey4K1zOU3/view?usp=sharing).
Here’s a step-by-step breakdown:
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

**Word2Vec Embedding API Integration**

Integrates a deployed Word2Vec API to generate embeddings for CV sections and job descriptions, enabling similarity calculation and scoring.([GitHub link](https://github.com/moghit-eou/Text-Classification-TF-IDF-Word2Vec-Embeddings)).

### 3. Cosine Similarity and Scoring

The relevance of a candidate is determined by comparing their CV to the job description.
1.  **Similarity Calculation**: The system calculates the **cosine similarity** between the vector of each CV section and the corresponding section of the job description. This measures the semantic similarity, not just keyword matching.
<p align="center">
  <img src="https://i.ibb.co/wqtg3Vw/image.png" alt="Cosine Similarity" width="500">
  <br>
</p>
For each section *i*, the cosine similarity is computed as:

$$
s_i = \cos(\theta) = \frac{v_i^{CV} \cdot v_i^{job}}{\|v_i^{CV}\| \times \|v_i^{job}\|}
$$


This measures the similarity between a CV section and the corresponding job description section.


2.  **Weighted Scoring**: Each section's similarity score is multiplied by a predefined weight (e.g., `work_experience` and `skills` are weighted higher).
 The overall CV score is the weighted average of the section scores:

$$
S_{CV} = \frac{\sum_i w_i \times s_i}{\sum_i w_i}
$$



3.  **Final Score**: The weighted scores are summed up to produce a final, global score for the candidate.

### 4. Data Storage and Visualization

1.  **Storage & Scoring**: The structured CV, along with its detailed and final scores, is saved as a document in a MongoDB database.
<details>
  <summary>📄 MongoDB Document (JSON Resume)</summary>
  <p align="center">
    <img src="https://i.ibb.co/JRktny9P/image.png" alt="MongoDB Resume Document" width="600">
    <br>
    <em>Example of a stored resume document in MongoDB.</em>
  </p>
</details>

<p align="center">
  <img src="https://i.ibb.co/dsg1dV8r/image.png" alt="Resume received via email" width="500">
  <br>
  <em>Example: A resume received as an email attachment ready for processing.</em>
</p>


2.  **Display**: A user can navigate to the Flask application's `/get_resume` endpoint, which retrieves all candidates from MongoDB, sorts them by their final score in descending order, and displays them on a clean, user-friendly web page.

<p align="center">
  <img src="https://i.ibb.co/dyRJQvb/image.png" alt="Candidate Leaderboard" width="700">
  <br>
  <em>Final web application showing ranked candidates.</em>
</p>

---
<a id="installation"></a>

##  Installation

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
    docker run -p 7860:7860 resume-scorer
    ```

---

## 📖 Usage

1.  **Deploy the Models**: Ensure your classification and vectorization models are deployed (e.g., on Hugging Face Spaces) and that the API endpoints are accessible.
2.  **Configure n8n**: Import the workflow JSON file into your n8n instance. Update the `HTTP Request` nodes with your deployed model URLs and the Flask application's endpoint.
3.  **Start the Process**: Send an email with a CV attached to the monitored Gmail account.
4.  **View Results**: Open your browser and navigate to `URL/get_resume` to see the ranked list of candidates.



## 📄 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute with attribution.

<div align="center">
  <h4>Happy Automating!</h4>
</div>

<div align="center">
  <h3>⭐ If you found this project useful, please give it a star!</h3>
  <a href="https://github.com/moghit-eou/semantic-NLP-resume-ranking">
    <img src="https://img.shields.io/github/stars/your-username/your-repo-name?style=social" alt="GitHub stars">
  </a>
</div>


