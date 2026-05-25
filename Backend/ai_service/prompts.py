def flashcards_prompt(text):
    return f"""
Generate 5 flashcards from this course content.

Return ONLY valid JSON in this format:
[
  {{
    "question": "...",
    "answer": "...",
    "difficulty": "easy"
  }}
]

Rules:
- difficulty must be easy, medium, or hard
- answers must be clear and short
- no text outside JSON

Course content:
{text}
"""


