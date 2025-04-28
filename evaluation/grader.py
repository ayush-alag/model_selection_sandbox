import re
from skill_tests.skill_test import SkillTest

def grade_answer(remote_model, test: SkillTest, answer: str) -> int:
    """
    Use the remote model to grade a local model's answer to a skill test.
    Returns a score from 1 to 10.
    """
    # Construct a grading prompt for the remote model
    context_part = f"Context:\n{test.context}\n" if test.context else ""
    expected_part = f"Expected answer: {test.expected}\n" if test.expected else ""
    grading_prompt = (
        f"You are a strict grader. Evaluate the following response.\n"
        f"{context_part}"
        f"Question: {test.question}\n"
        f"{expected_part}"
        f"Answer to evaluate: {answer}\n\n"
        f"On a scale of 1 to 10 (10 = completely correct and well-written, 1 = incorrect or irrelevant), "
        f"just output the numeric score."
    )
    messages = [{"role": "user", "content": grading_prompt}]
    grade_str = remote_model.generate_response(messages).strip()
    # Extract the first number from the response (expecting a number 1-10)
    match = re.search(r'\b(?:10|[1-9])\b', grade_str)
    if match:
        return int(match.group(0))
    else:
        # If parsing fails, default to 1 (worst) or attempt to interpret the response
        try:
            # If the remote model wrote something like "Score: 8/10", extract 8
            num_match = re.search(r'\d+', grade_str)
            return int(num_match.group(0)) if num_match else 1
        except:
            return 1