from rest_framework import serializers
from .models import CoursePDF, Deck, Flashcard, Quiz, QuizQuestion, QuizAttempt

class FlashcardSerializer(serializers.ModelSerializer):
    front = serializers.CharField(source="question")
    back = serializers.CharField(source="answer")

    class Meta:
        model = Flashcard
        fields = ["id", "front", "back", "difficulty"]


class DeckSerializer(serializers.ModelSerializer):
    cards = FlashcardSerializer(source="flashcards", many=True, read_only=True)
    subject = serializers.CharField(default="Depuis PDF")
    color = serializers.CharField(default="#8B6CF6")
    mastered = serializers.IntegerField(default=0)
    due = serializers.IntegerField(default=0)

    class Meta:
        model = Deck
        fields = ["id", "title", "subject", "color", "mastered", "due", "cards"]


class CoursePDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePDF
        fields = "__all__"

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = "__all__"


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = "__all__"