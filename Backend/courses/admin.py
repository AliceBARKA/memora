from django.contrib import admin

from .models import (
    CoursePDF,
    Deck,
    Flashcard,
    Quiz,
    QuizQuestion,
    QuizAttempt,
)

admin.site.register(CoursePDF)
admin.site.register(Deck)
admin.site.register(Flashcard)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAttempt)