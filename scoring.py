import json
import requests
import numpy as np

with open('job_description.json', 'r', encoding='utf-8') as f:
    job_description = json.load(f)

def resume_text_to_json(resume):
    clean_text = resume.encode().decode('unicode_escape')
    data = json.loads(clean_text)
    return data 


def get_vector(text):
    response = requests.get(f'https://moghit-word2vec-embeddings.hf.space/vectorization?text={text}')
    data = response.json()

    if 'vector' not in data:
        print(f"Error: 'vector' key not found for input: {text}")
        print("Full response:", data)
        return 0  # or handle error appropriately

    return data['vector']


def cosine_similarity(first_text, second_text):
    vec1 = get_vector(first_text)
    vec2 = get_vector(second_text)

    # dot(vec1, vec2) / (||vec1|| * ||vec2||)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0  # avoid division by zero

    return dot_product / (norm_vec1 * norm_vec2)

def get_score(json_resume):
    sections = ['professional_summary', 'work_experience', 'education', 'skills', 'others']
    scores = {}

    for section in sections:
        candidate_text = json_resume[section]
        job_text = job_description[section]
        scores[section] = cosine_similarity(candidate_text, job_text)

    overall_score = sum(scores.values()) / len(scores)
    return overall_score

def get_score_1(json_resume):
    sections = ['professional_summary', 'work_experience', 'education', 'skills', 'others']
    weights = {
        "professional_summary": 0.2,
        "work_experience": 0.4,
        "education": 0.1,
        "skills": 0.2,
        "others": 0.1
    }
    scores = {}

    weighted_sum = 0
    total_weight = 0

    for section in sections:
        candidate_text = json_resume[section]
        job_text = job_description[section]
        score = cosine_similarity(candidate_text, job_text)
        scores[section] = score

        weight = weights.get(section, 0)
        weighted_sum += score * weight
        total_weight += weight

    overall_score = weighted_sum / total_weight if total_weight != 0 else 0
    return overall_score
