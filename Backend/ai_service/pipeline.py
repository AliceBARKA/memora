import math
import re

from .text_cleaning import clean_text
from .chunking import build_balanced_contexts
from .flashcards import generate_flashcards_with_groq
from .similarity import contains_similar_text

GENERATION_BATCH_SIZE = 8
SOURCE_CHUNK_SIZE = 7000


def interleave_batches(batches):
    interleaved = []
    max_size = max((len(batch) for batch in batches), default=0)
    for index in range(max_size):
        for batch in batches:
            if index < len(batch):
                interleaved.append(batch[index])
    return interleaved


def evenly_select(items, count):
    if len(items) <= count:
        return items
    if count == 1:
        return [items[len(items) // 2]]
    return [
        items[round(index * (len(items) - 1) / (count - 1))]
        for index in range(count)
    ]


def build_flashcard_fallbacks(text, existing_cards, count, difficulty="all"):
    snippets = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if len(sentence.strip()) >= 30
    ]
    if not snippets:
        snippets = [text[index:index + 500].strip() for index in range(0, len(text), 500)]
    snippets = [snippet for snippet in snippets if snippet]
    snippets = evenly_select(snippets, max(1, count - len(existing_cards)))

    used_questions = [
        (card.get("question") or "").strip().lower()
        for card in existing_cards
        if isinstance(card, dict)
    ]
    fallback_difficulties = ["easy", "medium", "hard"]
    fallbacks = []
    missing = count - len(existing_cards)

    for index, snippet in enumerate(snippets):
        if len(fallbacks) >= missing:
            break
        preview = snippet[:140].rstrip()
        question = f"Explique ce passage du cours ({index + 1}) : {preview}"
        if contains_similar_text(question, used_questions):
            continue
        used_questions.append(question)
        fallbacks.append({
            "question": question,
            "answer": snippet[:700],
            "difficulty": (
                fallback_difficulties[index % len(fallback_difficulties)]
                if difficulty == "all"
                else difficulty
            ),
        })

    return fallbacks


def add_unique_cards(target, cards, seen_questions):
    for card in cards or []:
        if not isinstance(card, dict):
            continue
        question = (card.get("question") or "").strip()
        if question and not contains_similar_text(question, seen_questions):
            seen_questions.append(question)
            target.append(card)


def request_flashcards(chunk, count, difficulty, focus):
    try:
        return generate_flashcards_with_groq(
            chunk,
            count=count,
            difficulty=difficulty,
            focus=focus,
        )
    except Exception:
        return []


def generate_flashcards_pipeline(text, count=10, difficulty="all", focus=""):
    cleaned_text = clean_text(text)
    source_chunks = build_balanced_contexts(
        cleaned_text,
        max_contexts=min(12, max(1, count)),
        chunk_chars=SOURCE_CHUNK_SIZE,
    )

    all_flashcards = []
    seen_questions = []

    if not source_chunks:
        return []

    cards_per_chunk = max(1, math.ceil(count / len(source_chunks)))
    first_pass_batches = []
    for chunk in source_chunks:
        first_pass_batches.append(request_flashcards(
            chunk,
            min(cards_per_chunk, GENERATION_BATCH_SIZE),
            difficulty,
            focus,
        ))
    add_unique_cards(all_flashcards, interleave_batches(first_pass_batches), seen_questions)

    max_retries = math.ceil(count / GENERATION_BATCH_SIZE) + 3

    no_progress_attempts = 0
    for attempt in range(max_retries):
        remaining = count - len(all_flashcards)
        if remaining <= 0:
            break
        chunk = source_chunks[attempt % len(source_chunks)]
        retry_focus = focus
        if all_flashcards:
            previous_questions = "; ".join(
                card["question"] for card in all_flashcards[-10:]
            )
            retry_focus = (
                f"{focus} Évite absolument ces questions déjà générées : "
                f"{previous_questions}"
            ).strip()
        cards = request_flashcards(
            chunk,
            min(remaining, GENERATION_BATCH_SIZE),
            difficulty,
            retry_focus,
        )
        before_count = len(all_flashcards)
        add_unique_cards(all_flashcards, cards, seen_questions)
        if len(all_flashcards) == before_count:
            no_progress_attempts += 1
            if no_progress_attempts >= 2:
                break
        else:
            no_progress_attempts = 0

    selected_cards = evenly_select(all_flashcards, count)
    if len(selected_cards) < count:
        selected_cards.extend(
            build_flashcard_fallbacks(cleaned_text, selected_cards, count, difficulty)
        )
    return selected_cards[:count]
