from rest_framework import serializers
from .models import (
    CoursePDF,
    Deck,
    Flashcard,
    Quiz,
    QuizQuestion,
    QuizAttempt,
    Folder
)

ABSOLUTE_MAX_QUIZ_COUNT = 40


class DeckQuizGenerationSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=False, min_value=1)
    difficulty = serializers.ChoiceField(
        choices=["all", "easy", "medium", "hard"],
        default="all",
    )
    instructions = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        max_length=500,
    )
    focus = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
        max_length=500,
    )

    def validate(self, attrs):
        maximum = min(self.context["flashcard_count"], ABSOLUTE_MAX_QUIZ_COUNT)
        attrs["count"] = attrs.get("count", min(10, maximum))
        if not attrs.get("instructions") and attrs.get("focus"):
            attrs["instructions"] = attrs["focus"]
        attrs.pop("focus", None)
        return attrs

    def validate_count(self, count):
        flashcard_count = self.context["flashcard_count"]
        maximum = min(flashcard_count, ABSOLUTE_MAX_QUIZ_COUNT)
        if count > maximum:
            raise serializers.ValidationError(
                f"Le nombre de questions ne peut pas dépasser {maximum} pour ce deck."
            )
        return count


class FolderSerializer(serializers.ModelSerializer):
    courses_count = serializers.SerializerMethodField()

    def get_courses_count(self, obj):
        return obj.courses.count()

    class Meta:
        model = Folder
        fields = ["id", "name", "courses_count", "created_at"]

class FlashcardSerializer(serializers.ModelSerializer):
    front = serializers.CharField(source="question")
    back = serializers.CharField(source="answer")

    class Meta:
        model = Flashcard
        fields = ["id", "front", "back", "difficulty"]


class ManualFlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ["id", "question", "answer", "difficulty"]
        read_only_fields = ["id"]

    def validate_question(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("La question est obligatoire.")
        return value

    def validate_answer(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("La réponse est obligatoire.")
        return value


class DeckSerializer(serializers.ModelSerializer):
    cards = FlashcardSerializer(source="flashcards", many=True, read_only=True)
    subject = serializers.CharField(default="Depuis PDF")
    color = serializers.CharField(default="#8B6CF6")
    mastered = serializers.IntegerField(default=0)
    due = serializers.IntegerField(default=0)

    class Meta:
        model = Deck
        fields = [
            "id",
            "title",
            "subject",
            "color",
            "mastered",
            "due",
            "cards",
        ]


class CoursePDFSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()

    def get_file_name(self, obj):
        return obj.file.name.rsplit("/", 1)[-1]

    class Meta:
        model = CoursePDF
        fields = ["id", "title", "subject", "file_name", "summary", "uploaded_at"]
        read_only_fields = fields


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ["id", "question", "choices"]


class QuizSerializer(serializers.ModelSerializer):
    quiz_questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "subject", "deck", "course", "created_at", "quiz_questions"]
        read_only_fields = fields


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = "__all__"
        read_only_fields = fields
