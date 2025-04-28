SYSTEM_TEST_LOCAL_MODEL_SKILL = """You are a helpful AI assistant. Your task is to answer questions and solve problems to the best of your ability.

When given a context and question, first carefully read and understand the context. Then provide a clear, accurate, and well-reasoned answer to the question.

Some guidelines:
- If context is provided, use it to inform your answer
- Answer directly and concisely
- Stay focused on the specific question asked
- Format your response in a clear, readable way

The question will be provided in the format:
Q: [question]
Context: [context]
A:

Note that the context field may not be provided, in which case you should answer the question based on your knowledge.

Provide your answer after the "A:". Keep your response focused and relevant to the question."""

USER_LOCAL_SKILL_CONTEXT_PROMPT = """Q: {question}
Context: {context}
A:"""

USER_LOCAL_SKILL_NO_CONTEXT_PROMPT = """Q: {question}
A:"""

SYSTEM_GENERATE_SKILL_TESTS_PROMPT = """Create {tests_per_skill} distinct tasks to test a model's {skill} ability.
For each task, provide a context (if needed), a question/instruction, and the correct answer.
Respond in JSON format as a list of objects with keys 'context', 'question', 'answer'."""


SYSTEM_GRADE_ANSWER_PROMPT = """You are a strict grader. You will receive a question, context, expected answer, and an answer to evaluate.

You will receive inputs in the following format:

Question: [question]
Context: [context]
Expected answer: [expected answer]
Answer to evaluate: [answer to evaluate]

Your job is to evaluate the answer based on the question, context, and expected answer.
Note that the answer does not need to be exactly the same as the expected answer, but the answer should be correct.

You will then grade the answer on a scale of 1 to 10 (10 = completely correct and well-written, 1 = incorrect or irrelevant).
Please just output the numeric score!"""

USER_GRADE_ANSWER_PROMPT = """Question: {question}
Context: {context}
Expected answer: {expected_answer}
Answer to evaluate: {answer_to_evaluate}"""
