from skill_tests.skill_test import SkillTest

# Predefined static skill tests covering different skills
STATIC_SKILL_TESTS: list[SkillTest] = []

# Summarization skill tests
STATIC_SKILL_TESTS.append(SkillTest(
    skill="summarization",
    context=("Climate change refers to long-term shifts in temperatures and weather patterns. "
             "These shifts may be natural, but since the 1800s, human activities have been the main driver, "
             "primarily due to burning fossil fuels like coal, oil and gas."),
    question="Summarize the above paragraph in one sentence.",
    expected="Human-induced climate change is causing long-term shifts in temperatures and weather patterns."
))
STATIC_SKILL_TESTS.append(SkillTest(
    skill="summarization",
    context=("Artificial intelligence, or AI, is a field of computer science that focuses on creating systems "
             "capable of performing tasks that typically require human intelligence. "
             "This includes learning from data, recognizing patterns, and making decisions."),
    question="Provide a one-sentence summary of the above text.",
    expected="Artificial intelligence is a field of computer science that creates systems able to perform tasks requiring human-like intelligence."
))

# Extraction skill tests
STATIC_SKILL_TESTS.append(SkillTest(
    skill="extraction",
    context="Alice was born in 1990 and Bob was born in 1985. They both live in New York City.",
    question="What year was Alice born?",
    expected="1990"
))
STATIC_SKILL_TESTS.append(SkillTest(
    skill="extraction",
    context="The museum is open from 9 AM to 5 PM, and the entry fee is $15 for adults and $10 for children.",
    question="How much is the entry fee for children?",
    expected="$10"
))

# Reasoning skill tests
STATIC_SKILL_TESTS.append(SkillTest(
    skill="reasoning",
    context="",
    question="John is twice as old as Mary. Together, their ages sum to 36. How old is John?",
    expected="24"
))
STATIC_SKILL_TESTS.append(SkillTest(
    skill="reasoning",
    context="",
    question="If a rectangle has length 5 and width 3, what is its area?",
    expected="15"
))