import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in Backend/.env")

client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"


def extract_json_array(text):
    """
    Extracts and parses a JSON array from an AI response.
    Returns [] if parsing fails.
    """

    if not text:
        return []

    cleaned = text.strip()

    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    match = re.search(r"\[.*\]", cleaned, re.DOTALL)

    if not match:
        print("No JSON array found in AI response:")
        print(cleaned)
        return []

    json_text = match.group(0)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
        print("Raw AI response:")
        print(cleaned)
        return []


def generate_flashcards_with_groq(text):
    prompt = f"""
Tu es un assistant pédagogique.

Génère EXACTEMENT 10 flashcards à partir du cours suivant.

Réponds uniquement avec un tableau JSON valide.
Ne mets aucun texte avant ou après le JSON.
Ne mets pas de markdown.
Ne mets pas de ```.

Format obligatoire:
[
  {{
    "question": "question claire",
    "answer": "réponse courte et correcte",
    "difficulty": "easy"
  }}
]

Contraintes:
- difficulty doit être exactement: easy, medium ou hard
- évite les questions administratives inutiles
- privilégie les notions importantes du cours
- réponds en français
- aucun champ supplémentaire

Cours:
{text[:8000]}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Tu réponds uniquement avec un tableau JSON valide."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content
    cards = extract_json_array(content)

    valid_cards = []

    for card in cards:
        question = card.get("question")
        answer = card.get("answer")
        difficulty = card.get("difficulty", "medium")

        if not question or not answer:
            continue

        if difficulty not in ["easy", "medium", "hard"]:
            difficulty = "medium"

        valid_cards.append({
            "question": question,
            "answer": answer,
            "difficulty": difficulty,
        })

    return valid_cards


def generate_summary_with_groq(text):
    prompt = f"""
Tu es un assistant pédagogique.

Résume le cours suivant de manière claire et structurée.

Contraintes:
- réponds en français
- garde les notions importantes
- utilise des titres
- explique simplement
- ne rajoute pas d'informations inventées
- évite les détails administratifs inutiles

Cours:
{text[:10000]}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant pédagogique clair et structuré."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def generate_quiz_with_groq(flashcards):
    prompt = f"""
Tu es un assistant pédagogique.

À partir des flashcards suivantes, génère EXACTEMENT 10 questions de quiz QCM.

Réponds uniquement avec un tableau JSON valide.
Ne mets aucun texte avant ou après le JSON.
Ne mets pas de markdown.
Ne mets pas de ```.

Format obligatoire:
[
  {{
    "question": "question claire",
    "choices": ["choix A", "choix B", "choix C", "choix D"],
    "correct_answer": "choix A",
    "explanation": "explication courte"
  }}
]

Contraintes strictes:
- chaque question doit avoir exactement 4 choix
- correct_answer doit être exactement égal à l'un des 4 choix
- une seule bonne réponse
- questions claires
- réponds en français
- aucun champ supplémentaire

Flashcards:
{json.dumps(flashcards, ensure_ascii=False)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Tu réponds uniquement avec un tableau JSON valide. Aucun markdown."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content
    questions = extract_json_array(content)

    valid_questions = []

    for question in questions:
        q_text = question.get("question")
        choices = question.get("choices")
        correct_answer = question.get("correct_answer")
        explanation = question.get("explanation", "")

        if not q_text or not choices or not correct_answer:
            continue

        if not isinstance(choices, list):
            continue

        if len(choices) != 4:
            continue

        if correct_answer not in choices:
            continue

        valid_questions.append({
            "question": q_text,
            "choices": choices,
            "correct_answer": correct_answer,
            "explanation": explanation,
        })

    return valid_questions