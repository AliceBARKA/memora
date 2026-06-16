from .openai_service import call_openai_json
from .parsing import extract_json_array, extract_json_lines
from .prompts import (
    JSON_ONLY_SYSTEM,
    build_flashcard_facts_prompt,
    build_flashcards_from_facts_prompt,
    build_flashcards_prompt,
)
from .validators import validate_flashcards


def generate_flashcards_with_openai(text, count=10, difficulty="all", focus=""):
    content = call_openai_json(
        build_flashcards_prompt(text, count, difficulty, focus),
        JSON_ONLY_SYSTEM,
        temperature=0.1,
    )
    return validate_flashcards(extract_json_array(content))


def extract_flashcard_facts_with_openai(text, fact_count=8, focus=""):
    content = call_openai_json(
        build_flashcard_facts_prompt(text, fact_count, focus),
        JSON_ONLY_SYSTEM,
        temperature=0.1,
    )
    return extract_json_lines(content, "facts")[:fact_count]


def generate_flashcards_from_facts_with_openai(
    facts,
    count,
    difficulty="all",
    focus="",
    previous_questions=None,
):
    content = call_openai_json(
        build_flashcards_from_facts_prompt(
            facts,
            count,
            difficulty,
            focus,
            previous_questions,
        ),
        JSON_ONLY_SYSTEM,
        temperature=0.1,
    )
    return validate_flashcards(extract_json_array(content))[:count]
