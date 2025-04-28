import matplotlib.pyplot as plt

def plot_skill_levels(scores: dict, save_path: str = "skill_levels.png"):
    """
    Create a boxplot to visualize the distribution of skill scores for each model per skill.
    Saves the plot to the given path (or shows it if no path provided).
    """
    skills = sorted({skill for model_scores in scores.values() for skill in model_scores.keys()})
    num_skills = len(skills)
    # Prepare subplots: one boxplot per skill
    fig, axes = plt.subplots(1, num_skills, figsize=(6 * num_skills, 5), squeeze=False)
    axes = axes[0]  # as we created 1 row
    for i, skill in enumerate(skills):
        data = []
        labels = []
        # Collect score lists for each model for this skill
        for model_name, skill_dict in scores.items():
            if skill in skill_dict and len(skill_dict[skill]) > 0:
                data.append(skill_dict[skill])
                labels.append(model_name)
        if not data:
            # If no data for this skill, skip plotting it
            continue
        axes[i].boxplot(data, notch=False, patch_artist=True)
        axes[i].set_title(f"Skill: {skill}")
        axes[i].set_xticklabels(labels, rotation=30, ha='right')
        axes[i].set_ylim(0, 10)
        axes[i].set_ylabel("Score")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()