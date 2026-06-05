from datetime import datetime, timedelta

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Availability, RevisionPlan, RevisionSession
from .serializers import (
    AvailabilitySerializer,
    RevisionPlanSerializer,
    RevisionSessionSerializer,
)

from courses.models import Deck
from todos.models import ToDo
from ai_service.groq_service import generate_revision_plan_with_groq


DAY_TO_WEEKDAY = {
    "Lundi": 0,
    "Mardi": 1,
    "Mercredi": 2,
    "Jeudi": 3,
    "Vendredi": 4,
    "Samedi": 5,
    "Dimanche": 6,
}


def get_current_user(request):
    if request.user and request.user.is_authenticated:
        return request.user

    user = User.objects.first()
    if user is None:
        user = User.objects.create_user(username="demo", password="demo1234")

    return user


def find_date_before_exam(day_name, exam_date):
    target_weekday = DAY_TO_WEEKDAY.get(day_name)

    if target_weekday is None:
        return exam_date

    current_date = exam_date

    for _ in range(14):
        if current_date.weekday() == target_weekday:
            return current_date
        current_date -= timedelta(days=1)

    return exam_date


@api_view(["GET", "POST"])
def revision_plan_create(request):
    user = get_current_user(request)

    if request.method == "GET":
        plans = RevisionPlan.objects.filter(user=user).order_by("-created_at")
        serializer = RevisionPlanSerializer(plans, many=True)
        return Response(serializer.data)

    serializer = RevisionPlanSerializer(data={**request.data, "user": user.id})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
def availability_list_create(request):
    user = get_current_user(request)

    if request.method == "GET":
        availabilities = Availability.objects.filter(user=user)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)

    serializer = AvailabilitySerializer(data={**request.data, "user": user.id})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
def revision_session_list_create(request):
    user = get_current_user(request)

    if request.method == "GET":
        sessions = RevisionSession.objects.filter(
            revisionPlan__user=user
        ).order_by("-date")

        serializer = RevisionSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    serializer = RevisionSessionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["POST"])
def generate_ai_revision_plan(request):
    user = get_current_user(request)

    deck_id = request.data.get("deck_id")
    exam_date_raw = request.data.get("exam_date")
    priority = request.data.get("priority", "medium")

    if priority not in ["low", "medium", "high"]:
        priority = "medium"

    if not deck_id or not exam_date_raw:
        return Response({
            "error": "deck_id et exam_date sont obligatoires"
        }, status=400)

    try:
        exam_date = datetime.strptime(exam_date_raw, "%Y-%m-%d").date()
    except ValueError:
        return Response({
            "error": "exam_date doit être au format YYYY-MM-DD"
        }, status=400)

    try:
        deck = Deck.objects.prefetch_related("flashcards").get(id=deck_id)
    except Deck.DoesNotExist:
        return Response({"error": "Deck introuvable"}, status=404)

    availabilities = Availability.objects.filter(user=user)

    if not availabilities.exists():
        return Response({
            "error": "Aucune disponibilité trouvée"
        }, status=400)

    flashcards_data = [
        {
            "question": card.question,
            "answer": card.answer,
            "difficulty": card.difficulty,
        }
        for card in deck.flashcards.all()
    ]

    availabilities_data = [
        {
            "day": availability.day,
            "start_time": availability.start_time.strftime("%H:%M"),
            "end_time": availability.end_time.strftime("%H:%M"),
        }
        for availability in availabilities
    ]

    try:
        ai_sessions = generate_revision_plan_with_groq(
            deck_title=deck.title,
            flashcards=flashcards_data,
            availabilities=availabilities_data,
            exam_date=exam_date_raw,
            priority=priority,
        )
    except Exception as e:
        return Response({
            "error": "Erreur pendant la génération du planning IA",
            "details": str(e)
        }, status=500)

    if not ai_sessions:
        return Response({
            "error": "Aucune séance générée par l'IA"
        }, status=400)

    revision_plan = RevisionPlan.objects.create(
        title=f"Planning IA - {deck.title}",
        description="Planning de révision généré automatiquement par l'IA",
        exam_date=exam_date,
        priority=priority,
        goal=f"Réviser {deck.title} avant l'examen",
        user=user,
    )

    created_sessions = []

    for ai_session in ai_sessions:
        day = ai_session["day"]
        matching_availability = availabilities.filter(day=day).first()

        if not matching_availability:
            continue

        session_date = find_date_before_exam(day, exam_date)

        session = RevisionSession.objects.create(
            revisionPlan=revision_plan,
            deck=deck,
            date=session_date,
            start_time=ai_session["start_time"],
            end_time=ai_session["end_time"],
            status="planned",
        )

        todo = ToDo.objects.create(
            title=ai_session["todo_title"],
            description=ai_session["todo_description"],
            priority=ai_session["todo_priority"],
            due_date=session_date,
            user=user,
            revision_session=session,
        )

        created_sessions.append({
            "session_id": session.id,
            "todo_id": todo.id,
            "day": day,
            "date": session_date,
            "start_time": ai_session["start_time"],
            "end_time": ai_session["end_time"],
            "objective": ai_session["objective"],
            "session_type": ai_session["session_type"],
        })

    return Response({
        "message": "Planning IA généré avec succès",
        "revision_plan_id": revision_plan.id,
        "sessions_count": len(created_sessions),
        "sessions": created_sessions,
    }, status=201)