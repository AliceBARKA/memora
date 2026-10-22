# Modèle relationnel — Memora

USERS(
    id PK,
    username,
    email,
    password,
    role,
    is_active
)

FOLDER(
    id PK,
    name,
    created_at,
    user_id FK
)

COURSE_PDF(
    id PK,
    title,
    subject,
    file,
    summary,
    uploaded_at,
    user_id FK,
    folder_id FK
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
    subject,
    created_at,
    deck_id FK
)

QUIZ_QUESTION(
    id PK,
    question,
    correct_answer,
    choices,
    quiz_id FK
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
    description,
    created_at,
    user_id FK
)

REVISION_SESSION(
    id PK,
    revision_date,
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

FORUM_POST(
    id PK,
    title,
    content,
    created_at,
    user_id FK
)

FORUM_COMMENT(
    id PK,
    content,
    created_at,
    user_id FK,
    post_id FK
)

AI_CONVERSATION(
    id PK,
    title,
    scope,
    created_at,
    user_id FK,
    course_pdf_id FK
)

AI_MESSAGE(
    id PK,
    role,
    content,
    created_at,
    conversation_id FK
)