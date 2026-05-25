from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CoursePDF, Deck, Quiz,Flashcard
from .serializers import CoursePDFSerializer, DeckSerializer, QuizSerializer
import fitz 
from ai_service.gemini_service import (
    generate_flashcards_with_gemini,
    generate_summary_with_gemini,
    ask_pdf_with_gemini,
    generate_quiz_with_gemini,
    generate_personal_quiz_with_gemini,
)


@api_view(["GET"])
def get_courses(request):
    courses = CoursePDF.objects.filter(
    user=request.user
)
    serializer = CoursePDFSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def upload_course(request):
    user = request.user

    title = request.data.get("title", "Nouveau cours")
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "Aucun fichier PDF envoyé"}, status=400)

    course = CoursePDF.objects.create(
        title=title,
        file=file,
        user=user
    )

    serializer = CoursePDFSerializer(course)
    return Response(serializer.data, status=201)

@api_view(["GET"])
def get_decks(request):
    decks = Deck.objects.prefetch_related(
    "flashcards"
).filter(user=request.user)
    serializer = DeckSerializer(decks, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def generate_flashcards_from_course(request, course_id):
    try:
        course = CoursePDF.objects.get(id=course_id, user=request.user)
        existing_deck = Deck.objects.filter(
    CoursePDF=course,
    user=request.user
).first()

        if existing_deck:
            return Response({
                "already_exists": True,
                "deck_id": existing_deck.id,
                "message": "Flashcards déjà générées."
        })

    except CoursePDF.DoesNotExist:
        return Response({"error": "Cours introuvable"}, status=404)

    text = ""

    with fitz.open(course.file.path) as pdf:
        for page in pdf:
            text += page.get_text()

    if not text.strip():
        return Response({"error": "Impossible d'extraire le texte du PDF"}, status=400)

    generated_cards = generate_flashcards_with_gemini(text[:12000])
    print("FLASHCARDS GEMINI =", generated_cards)

    deck = Deck.objects.create(
        title=f"Flashcards - {course.title}",
        description="Flashcards générées automatiquement par l'IA",
        user=course.user,
        CoursePDF=course,
    )

    for card in generated_cards:
        Flashcard.objects.create(
            deck=deck,
            question=card.get("question", ""),
            answer=card.get("answer", ""),
            difficulty=card.get("difficulty", "medium"),
        )

    return Response({
    "already_exists": False,
    "deck_id": deck.id,
    "message": "Flashcards générées."
})



@api_view(["DELETE"])
def delete_course(request, course_id):
    try:
        course = CoursePDF.objects.get(id=course_id, user=request.user)
    except CoursePDF.DoesNotExist:
        return Response({"error": "Cours introuvable"}, status=404)

    course.delete()
    return Response({"message": "Cours supprimé"})


@api_view(["POST"])
def generate_summary_from_course(request, course_id):
    try:
        course = CoursePDF.objects.get(id=course_id, user=request.user)
    except CoursePDF.DoesNotExist:
        return Response({"error": "Cours introuvable"}, status=404)

    text = ""

    with fitz.open(course.file.path) as pdf:
        for page in pdf:
            text += page.get_text()

    if not text.strip():
        return Response({"error": "Impossible d'extraire le texte du PDF"}, status=400)

    summary = generate_summary_with_gemini(text[:12000])

    course.summary = summary
    course.save()

    serializer = CoursePDFSerializer(course)
    return Response(serializer.data)



@api_view(["POST"])
def ask_question_from_course(request, course_id):
    question = request.data.get("question", "")

    if not question.strip():
        return Response({"error": "Question vide"}, status=400)

    try:
        course = CoursePDF.objects.get(id=course_id, user=request.user)
    except CoursePDF.DoesNotExist:
        return Response({"error": "Cours introuvable"}, status=404)

    text = ""

    with fitz.open(course.file.path) as pdf:
        for page in pdf:
            text += page.get_text()

    if not text.strip():
        return Response({"error": "Impossible d'extraire le texte du PDF"}, status=400)

    answer = ask_pdf_with_gemini(text[:12000], question)

    return Response({
        "question": question,
        "answer": answer,
    })

from rest_framework import status

@api_view(["DELETE"])
def delete_deck(request, deck_id):
    try:
        deck = Deck.objects.get(id=deck_id, user=request.user)
    except Deck.DoesNotExist:
        return Response({"error": "Deck introuvable"}, status=404)

    deck.delete()
    return Response({"message": "Deck supprimé"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def generate_quiz_from_course(request, course_id):
    try:
        course = CoursePDF.objects.get(id=course_id, user=request.user)
    except CoursePDF.DoesNotExist:
        return Response({"error": "Cours introuvable"}, status=404)

    text = ""

    with fitz.open(course.file.path) as pdf:
        for page in pdf:
            text += page.get_text()

    if not text.strip():
        return Response({"error": "Impossible d'extraire le texte du PDF"}, status=400)

    questions = generate_quiz_with_gemini(text[:12000])

    quiz = Quiz.objects.create(
    title=f"Quiz - {course.title}",
    subject="Depuis PDF",
    questions=questions,
    user=course.user,
    course=course,
)

    serializer = QuizSerializer(quiz)
    return Response(serializer.data)


@api_view(["POST"])
def generate_personal_quiz(request):
    topic = request.data.get("topic", "")

    if not topic.strip():
        return Response({"error": "Sujet vide"}, status=400)

    questions = generate_personal_quiz_with_gemini(topic)

    user = request.user

    quiz = Quiz.objects.create(
        title=topic,
        subject="Personnalisé",
        questions=questions,
        user=user,
    )

    serializer = QuizSerializer(quiz)
    return Response(serializer.data)


@api_view(["GET"])
def get_quizzes(request):
    quizzes = Quiz.objects.filter(user=request.user)
    serializer = QuizSerializer(quizzes,many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_quiz(request,quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id, user=request.user)
    except Quiz.DoesNotExist:
        return Response({"error":"Quiz introuvable"},status=404)
    quiz.delete()
    return Response({"message": "Quiz supprimé"})
