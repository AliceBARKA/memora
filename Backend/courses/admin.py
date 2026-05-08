from django.contrib import admin
from .models import CoursePDF, Deck, Flashcard
# Register your models here.

admin.site.register(CoursePDF)
admin.site.register(Deck)
admin.site.register(Flashcard)