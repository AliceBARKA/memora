from django.urls import path
from .views import (
    get_courses,
    get_decks,
    upload_course,
    generate_flashcards_from_course,
    generate_summary_from_course,
    generate_quiz_from_deck,
    submit_quiz,
    quiz_attempt_history,
    quiz_statistics,
    
)

urlpatterns = [
    path("", get_courses, name="get_courses"),
    path("upload/", upload_course, name="upload_course"),
    path("decks/", get_decks, name="get_decks"),

    path(
        "<int:course_id>/generate-flashcards/",
        generate_flashcards_from_course,
        name="generate_flashcards_from_course"
    ),
    path(
        "<int:course_id>/generate-summary/",
        generate_summary_from_course,
        name="generate_summary_from_course"
    ),
    path(
        "decks/<int:deck_id>/generate-quiz/",
        generate_quiz_from_deck,
        name="generate_quiz_from_deck"
    ),
    path(
        "quizzes/<int:quiz_id>/submit/",
        submit_quiz,
        name="submit_quiz"
    ),
    path(
        "quizzes/<int:quiz_id>/history/",
        quiz_attempt_history,
        name="quiz_attempt_history"
    ),

    path(
        "quizzes/<int:quiz_id>/statistics/",
        quiz_statistics,
        name="quiz_statistics"
    ),
]
