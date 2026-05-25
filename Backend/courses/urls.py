from django.urls import path
from .views import get_courses, get_decks, upload_course, delete_course, generate_flashcards_from_course, generate_summary_from_course, ask_question_from_course, delete_deck, generate_quiz_from_course,generate_personal_quiz,get_quizzes,delete_quiz
urlpatterns = [
    path("", get_courses),
    path("upload/", upload_course),
    path("decks/", get_decks),
    path("<int:course_id>/", delete_course),
    path("<int:course_id>/generate-flashcards/", generate_flashcards_from_course),
    path("<int:course_id>/generate-summary/", generate_summary_from_course),
    path("<int:course_id>/ask/", ask_question_from_course),
    path("flashcards/delete/<int:deck_id>/", delete_deck),
    path("<int:course_id>/generate-quiz/", generate_quiz_from_course),
    path("generate-personal-quiz/", generate_personal_quiz),
    path("quizzes/", get_quizzes),
    path("quizzes/delete/<int:quiz_id>/",delete_quiz)
]