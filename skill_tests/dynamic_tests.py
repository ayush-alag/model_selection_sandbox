import json
from skill_tests.skill_test import SkillTest
from prompts.skill_prompts import SYSTEM_GENERATE_SKILL_TESTS_PROMPT

def generate_skill_tests(remote_model, skills: list[str], tests_per_skill: int = 1) -> list[SkillTest]:
    """
    Use the remote model to dynamically generate skill test tasks.
    For each skill in the list, requests the remote model to create a number of tasks.
    Returns a list of SkillTest instances.
    """
    generated_tests: list[SkillTest] = []
    for skill in skills:
        messages = [{"role": "user",
                     "content": SYSTEM_GENERATE_SKILL_TESTS_PROMPT.format(tests_per_skill=tests_per_skill, skill=skill)}]

        response = remote_model.generate_response(messages)
        # Try to parse the response as JSON
        try:
            tasks_data = json.loads(response)
        except json.JSONDecodeError:
            # If parsing fails, attempt to fix common issues or fall back to simpler parsing
            try:
                # Sometimes the model might wrap JSON in markdown or have trailing text
                json_str = response.strip().strip("```").strip()
                tasks_data = json.loads(json_str)
            except Exception as e:
                # If still failing, skip this skill
                print(f"Failed to parse generated tasks for skill '{skill}': {e}")
                continue
        # If parsed successfully and is a list, convert to SkillTest instances
        if isinstance(tasks_data, list):
            for task_item in tasks_data:
                if not isinstance(task_item, dict):
                    continue
                context = task_item.get("context", "")
                question = task_item.get("question", "")
                answer = task_item.get("answer", None)
                if question:
                    generated_tests.append(SkillTest(skill=skill, context=context, question=question, expected=answer))
    return generated_tests