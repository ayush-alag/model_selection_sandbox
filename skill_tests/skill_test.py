from dataclasses import dataclass
from typing import Optional

@dataclass
class SkillTest:
    """
    Data structure for a skill evaluation task.
    """
    skill: str            # The skill being tested (e.g., "summarization", "extraction", "reasoning").
    context: str          # Context or content on which the task is based (can be empty if not needed).
    question: str         # The instruction or question for the task.
    expected: Optional[str] = None  # The expected correct answer or ideal output (if known).