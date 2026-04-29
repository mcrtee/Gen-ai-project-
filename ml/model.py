import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# fake dataset (как будто kaggle)
jobs = {
    "Frontend Developer": ["JavaScript", "HTML", "CSS", "React", "UI/UX"],
    "Backend Developer": ["Python", "Django", "APIs", "Databases"],
    "AI Engineer": ["Python", "Machine Learning", "TensorFlow", "Data Science"]
}

def vectorize(skills, all_skills):
    return [1 if skill in skills else 0 for skill in all_skills]

def predict():
    with open("data/skills.json") as f:
        user_skills = json.load(f)["skills"]

    all_skills = list(set(sum(jobs.values(), []) + user_skills))

    user_vector = np.array(vectorize(user_skills, all_skills)).reshape(1, -1)

    results = []

    for job, skills in jobs.items():
        job_vector = np.array(vectorize(skills, all_skills)).reshape(1, -1)
        score = cosine_similarity(user_vector, job_vector)[0][0]

        missing = list(set(skills) - set(user_skills))

        results.append({
            "job": job,
            "score": float(score),
            "missing_skills": missing
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:3]


if __name__ == "__main__":
    print(json.dumps(predict(), indent=2))