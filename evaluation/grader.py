import re
from skill_tests.skill_test import SkillTest
from prompts.skill_prompts import SYSTEM_GRADE_ANSWER_PROMPT, USER_GRADE_ANSWER_PROMPT

def grade_answer(remote_model, grader_messages: list[dict], test: SkillTest, answer: str) -> int:
    """
    Use the remote model to grade a local model's answer to a skill test.
    Returns a score from 1 to 10.
    """
    # Construct a grading prompt for the remote model
    context_part = f"Context:\n{test.context}\n" if test.context else ""
    expected_part = f"Expected answer: {test.expected}\n" if test.expected else ""
    grading_prompt = USER_GRADE_ANSWER_PROMPT.format(question=test.question, context=context_part, expected_answer=expected_part, answer_to_evaluate=answer)
    grader_messages.append({"role": "user", "content": grading_prompt})

    grade_str = remote_model.generate_response(grader_messages).strip()

    # TODO: use a language model to parse the response?
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