import json

def generate_learning_plan(predictions):
    plans = []

    for p in predictions:
        for skill in p["missing_skills"]:
            plans.append({
                "skill": skill,
                "resource": f"Search YouTube: Learn {skill}"
            })

    return plans


if __name__ == "__main__":
    from ml.model import predict

    preds = predict()
    plan = generate_learning_plan(preds)

    print(json.dumps(plan, indent=2))