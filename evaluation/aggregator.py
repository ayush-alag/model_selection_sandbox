from typing import Dict, List

def summarize_scores(scores: Dict[str, Dict[str, List[int]]]) -> Dict[str, Dict[str, float]]:
    """
    Compute the average score per skill for each model.
    Returns a nested dictionary: { model_name: { skill: average_score, ... }, ... }.
    """
    summary: Dict[str, Dict[str, float]] = {}
    for model_name, skill_dict in scores.items():
        summary[model_name] = {}
        for skill, score_list in skill_dict.items():
            if len(score_list) > 0:
                summary[model_name][skill] = sum(score_list) / len(score_list)
            else:
                summary[model_name][skill] = None
    return summary