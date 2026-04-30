import json

def generate_learning_plan(predictions):
    """
    Инструкция для Antigravity: этот скрипт подготавливает ввод для LLM-агента.
    """
    prompt_for_agent = "User needs to learn these specific skills. Find real-world resources (GitHub, docs, hackathons): "
    
    plans = []
    for p in predictions:
        for skill in p["missing_skills"]:
            # В Antigravity агент увидит эту структуру и инициирует web_search
            plans.append({
                "skill": skill,
                "action_required": "RESEARCH_LIVE",
                "query": f"latest documentation and best github repos for {skill} 2026"
            })
    return plans