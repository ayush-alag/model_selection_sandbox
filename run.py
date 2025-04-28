import logging
from models.remote_model import RemoteModel
from models.local_model import LocalModel
from skill_tests.static_tests import STATIC_SKILL_TESTS
from skill_tests.dynamic_tests import generate_skill_tests
from evaluation import grader, aggregator
from visualization import plotter
import argparse
from collections import defaultdict
from prompts.skill_prompts import SYSTEM_GRADE_ANSWER_PROMPT

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("SkillEvaluationRunner")
    parser = argparse.ArgumentParser(description="Run skill evaluation")
    parser.add_argument("--dynamic", action="store_true", help="Use dynamic skill tests")
    args = parser.parse_args()

    # Configuration: choose static or dynamic skill tests
    NUM_DYNAMIC_TESTS_PER_SKILL = 2  # only used if USE_DYNAMIC_TESTS is True

    # TODO: Make this configurable
    # Initialize remote "supervisor" model (e.g., GPT-4 via OpenAI)
    remote_model = RemoteModel(name="GPT-4 Supervisor", model_name="gpt-4")

    # hardcoded: one GPT-3.5 Turbo and one Llama2 7B
    local_models = [
        LocalModel(name="GPT-3.5 Turbo", model_type="openai", model_name="gpt-3.5-turbo"),
        LocalModel(name="Llama2 7B", model_type="ollama", model_name="llama2")
    ]

    # Prepare skill tests (either static or dynamic)
    # TODO: maybe the remote model should choose which skills to test?
    if args.dynamic:
        skills_to_test = ["summarization", "extraction", "reasoning"]
        skill_tests = generate_skill_tests(remote_model, skills_to_test, tests_per_skill=NUM_DYNAMIC_TESTS_PER_SKILL)
        logger.info(f"Generated {len(skill_tests)} dynamic skill tests using the remote model.")
    else:
        # Use predefined static skill tests
        skill_tests = STATIC_SKILL_TESTS
        logger.info(f"Loaded {len(skill_tests)} static skill tests.")

    # Dictionary to collect scores: scores[model_name][skill] = [scores...]
    scores = {model.name: defaultdict(list) for model in local_models}
    for model in local_models:
        system_message = {"role": "system", "content": SYSTEM_GRADE_ANSWER_PROMPT}
        grader_messages = [system_message]

        for test in skill_tests:
            # Ensure each skill has a list initialized for this model
            answer = model.run_test(test)
            logger.info(f"{model.name} -> Task: {test.skill} | Question: {test.question} | Answer: {answer}")
            score = grader.grade_answer(remote_model, grader_messages, test, answer)
            scores[model.name][test.skill].append(score)
            logger.info(f"Graded score for {model.name} on {test.skill}: {score}/10")

    # Aggregate skill levels for each model (e.g., average score per skill)
    skill_summary = aggregator.summarize_scores(scores)
    print("Skill level summary (average scores):")
    for model_name, skill_dict in skill_summary.items():
        for skill, avg_score in skill_dict.items():
            avg_display = f"{avg_score:.2f}" if avg_score is not None else "N/A"
            print(f"  {model_name} - {skill}: {avg_display}")

    # Visualize skill level distributions for each model using boxplots
    plotter.plot_skill_levels(scores, save_path="skill_levels.png")
    print("Skill level boxplot saved to skill_levels.png")