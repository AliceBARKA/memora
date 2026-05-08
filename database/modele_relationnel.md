# Modèle relationnel — Memora

COURSE_PDF(
    id PK,
    title,
    file,
    uploaded_at,
    user_id FK
)

DECK(
    id PK,
    title,
    description,
    created_at,
    user_id FK,
    course_pdf_id FK
)

FLASHCARD(
    id PK,
    question,
    answer,
    difficulty,
    created_at,
    deck_id FK
)

QUIZ(
    id PK,
    title,
    created_at,
    deck_id FK
)

QUIZ_RESULT(
    id PK,
    score,
    correct_answers,
    passed_at,
    user_id FK,
    quiz_id FK
)

AVAILABILITY(
    id PK,
    day,
    start_time,
    end_time,
    user_id FK
)

REVISION_PLAN(
    id PK,
    title,
    created_at,
    user_id FK
)

REVISION_SESSION(
    id PK,
    date,
    start_time,
    end_time,
    status,
    revision_plan_id FK,
    deck_id FK
)

TODO(
    id PK,
    title,
    description,
    due_date,
    status,
    priority,
    user_id FK,
    revision_session_id FK
)