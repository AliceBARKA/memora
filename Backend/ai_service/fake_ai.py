def generate_fake_flashcards(text):
    return [
        {
            "question": "What is the main topic of this course?",
            "answer": text[:200],
            "difficulty": "easy"
        }
    ]