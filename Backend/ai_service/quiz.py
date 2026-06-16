import json
import math

from .chunking import evenly_select
from .openai_service import call_openai_json
from .parsing import extract_json_array
from .prompts import JSON_ONLY_SYSTEM, build_personal_quiz_prompt, build_quiz_prompt
from .validators import deduplicate_flashcards, validate_quiz_questions


QUIZ_BATCH_SIZE = 10


def _oversampled_count(count):
    return min(16, max(count + 3, math.ceil(count * 1.5)))


def _balanced_flashcard_batch(flashcards, attempt):
    subset_size = min(len(flashcards), QUIZ_BATCH_SIZE * 2)
    if subset_size == len(flashcards):
        return flashcards
    offset = (attempt * subset_size) % len(flashcards)
    rotated_flashcards = flashcards[offset:] + flashcards[:offset]
    return evenly_select(rotated_flashcards, subset_size)


def generate_quiz_with_openai(flashcards, count=10, difficulty="medium", instructions=""):
    distinct_flashcards = deduplicate_flashcards(flashcards)
    if not distinct_flashcards or count <= 0:
        return []

    all_questions = []
    max_attempts = math.ceil(count / QUIZ_BATCH_SIZE) + 2
    for attempt in range(max_attempts):
        missing_count = count - len(all_questions)
        if missing_count <= 0:
            break

        previous_questions = [question["question"] for question in all_questions]
        previous_instruction = (
            f"{instructions}\n"
            "Évite absolument les questions déjà générées suivantes: "
            f"{json.dumps(previous_questions, ensure_ascii=False)}"
        ).strip()
        content = call_openai_json(
            build_quiz_prompt(
                _balanced_flashcard_batch(distinct_flashcards, attempt),
                min(missing_count, QUIZ_BATCH_SIZE),
                difficulty,
                previous_instruction,
            ),
            JSON_ONLY_SYSTEM,
            temperature=0.1,
        )
        all_questions = validate_quiz_questions(
            all_questions + extract_json_array(content),
            count=count,
        )

    return validate_quiz_questions(all_questions, count=count)


def generate_personal_quiz_with_openai(topic, count=10, difficulty="medium", instructions=""):
    requested_count = _oversampled_count(count)
    content = call_openai_json(
        build_personal_quiz_prompt(topic, requested_count, difficulty, instructions),
        JSON_ONLY_SYSTEM,
        temperature=0.1,
    )
    return validate_quiz_questions(extract_json_array(content), count=count)
