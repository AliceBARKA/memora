from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CoursePDF, Deck, Flashcard, Quiz, QuizQuestion, QuizAttempt
from .serializers import CoursePDFSerializer, DeckSerializer

from ai_service.pdf_extractor import extract_text_from_pdf
from ai_service.pipeline import generate_flashcards_pipeline
from ai_service.groq_service import generate_summary_with_groq
from ai_service.groq_service import generate_quiz_with_groq

@api_view(["GET"])
def get_courses(request):
    courses = CoursePDF.objects.all().order_by("-uploaded_at")
    serializer = CoursePDFSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def upload_course(request):
    user = User.objects.first()
    if user is None:
        user = User.objects.create_user(username="demo", password="demo1234")

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
    decks = Deck.objects.prefetch_related("flashcards").all()
    serializer = DeckSerializer(decks, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def generate_flashcards_from_course(request, course_id):
    try:
        course = CoursePDF.objects.get(id=course_id)
    except CoursePDF.DoesNotExist:
        return Response({"error": "Cours introuvable"}, status=404)

    try:
        text = extract_text_from_pdf(course.file.path)
    except Exception as e:
        return Response({
            "error": "Erreur pendant l'extraction du PDF",
            "details": str(e)
        }, status=500)

    if not text.strip():
        return Response({
            "error": "Impossible d'extraire le texte du PDF"
        }, status=400)

    try:
        generated_cards = generate_flashcards_pipeline(text)
    except Exception as e:
        return Response({
            "error": "Erreur pendant la génération des flashcards",
            "details": str(e)
        }, status=500)

    if not generated_cards:
        return Response({
            "error": "Aucune flashcard générée"
        }, status=400)

    deck, created = Deck.objects.get_or_create(
        CoursePDF=course,
        user=course.user,
        defaults={
            "title": f"Flashcards - {course.title}",
            "description": "Flashcards générées automatiquement par l'IA",
        }
    )
    
    if not created:
        deck.flashcards.all().delete()

    for card in generated_cards:
        Flashcard.objects.create(
            deck=deck,
            question=card.get("question", ""),
            answer=card.get("answer", ""),
            difficulty=card.get("difficulty", "medium"),
        )

    return Response({
        "message": "Flashcards générées avec succès",
        "course_id": course.id,
        "deck_id": deck.id,
        "cards_count": len(generated_cards),
    }, status=201)

@api_view(["POST"])
def generate_summary_from_course(request, course_id):
    try:
        course = CoursePDF.objects.get(id=course_id)
    except CoursePDF.DoesNotExist:
        return Response({"error": "Cours introuvable"}, status=404)

    try:
        text = extract_text_from_pdf(course.file.path)
    except Exception as e:
        return Response({
            "error": "Erreur pendant l'extraction du PDF",
            "details": str(e)
        }, status=500)

    if not text.strip():
        return Response({
            "error": "Impossible d'extraire le texte du PDF"
        }, status=400)

    try:
        summary = generate_summary_with_groq(text)
    except Exception as e:
        return Response({
            "error": "Erreur pendant la génération du résumé",
            "details": str(e)
        }, status=500)

    course.summary = summary
    course.save()

    return Response({
        "message": "Résumé généré avec succès",
        "course_id": course.id,
        "summary": summary,
    }, status=201)


@api_view(["POST"])
def generate_quiz_from_deck(request, deck_id):
    try:
        deck = Deck.objects.get(id=deck_id)
    except Deck.DoesNotExist:
        return Response({"error": "Deck introuvable"}, status=404)

    flashcards = deck.flashcards.all()

    if not flashcards.exists():
        return Response({"error": "Aucune flashcard trouvée pour ce deck"}, status=400)

    flashcards_data = [
        {
            "question": card.question,
            "answer": card.answer,
            "difficulty": card.difficulty,
        }
        for card in flashcards
    ]

    try:
        generated_questions = generate_quiz_with_groq(flashcards_data)
    except Exception as e:
        return Response({
            "error": "Erreur pendant la génération du quiz",
            "details": str(e)
        }, status=500)

    if not generated_questions:
        return Response({"error": "Aucune question générée"}, status=400)

    quiz = Quiz.objects.create(
        title=f"Quiz - {deck.title}",
        deck=deck,
        user=deck.user,
    )

    for q in generated_questions:
        QuizQuestion.objects.create(
            quiz=quiz,
            question=q.get("question", ""),
            choices=q.get("choices", []),
            correct_answer=q.get("correct_answer", ""),
            explanation=q.get("explanation", ""),
        )

    return Response({
        "message": "Quiz généré avec succès",
        "deck_id": deck.id,
        "quiz_id": quiz.id,
        "questions_count": len(generated_questions),
    }, status=201)


@api_view(["POST"])
def submit_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.prefetch_related("questions").get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz introuvable"}, status=404)

    answers = request.data.get("answers", {})

    score = 0
    total = quiz.questions.count()
    corrections = []

    if total == 0:
        return Response({"error": "Ce quiz ne contient aucune question"}, status=400)

    for question in quiz.questions.all():
        user_answer = answers.get(str(question.id))
        is_correct = user_answer == question.correct_answer

        if is_correct:
            score += 1

        corrections.append({
            "question_id": question.id,
            "question": question.question,
            "choices": question.choices,
            "user_answer": user_answer,
            "correct_answer": question.correct_answer,
            "is_correct": is_correct,
            "explanation": question.explanation,
        })

    percentage = round((score / total) * 100, 2)

    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        user=quiz.user,
        score=score,
        total_questions=total,
        percentage=percentage,
    )

    return Response({
        "message": "Quiz corrigé avec succès",
        "quiz_id": quiz.id,
        "attempt_id": attempt.id,
        "score": score,
        "total_questions": total,
        "percentage": percentage,
        "corrections": corrections,
    }, status=201)

@api_view(["GET"])
def quiz_attempt_history(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz introuvable"}, status=404)

    attempts = QuizAttempt.objects.filter(quiz=quiz).order_by("-completed_at")

    data = [
        {
            "attempt_id": attempt.id,
            "score": attempt.score,
            "total_questions": attempt.total_questions,
            "percentage": attempt.percentage,
            "completed_at": attempt.completed_at,
        }
        for attempt in attempts
    ]

    return Response({
        "quiz_id": quiz.id,
        "quiz_title": quiz.title,
        "attempts": data,
    })


@api_view(["GET"])
def quiz_statistics(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz introuvable"}, status=404)

    attempts = QuizAttempt.objects.filter(quiz=quiz)

    if not attempts.exists():
        return Response({
            "quiz_id": quiz.id,
            "quiz_title": quiz.title,
            "attempts_count": 0,
            "best_score": None,
            "average_percentage": None,
            "last_percentage": None,
        })

    percentages = [attempt.percentage for attempt in attempts]

    return Response({
        "quiz_id": quiz.id,
        "quiz_title": quiz.title,
        "attempts_count": attempts.count(),
        "best_score": max(percentages),
        "average_percentage": round(sum(percentages) / len(percentages), 2),
        "last_percentage": attempts.order_by("-completed_at").first().percentage,
    })