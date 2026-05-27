from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Availability, RevisionPlan, RevisionSession
from .serializers import (
    AvailabilitySerializer,
    RevisionPlanSerializer,
    RevisionSessionSerializer,
)


@api_view(["GET", "POST"])
def revision_plan_create(request):
    if request.method == "GET":
        plans = RevisionPlan.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = RevisionPlanSerializer(plans, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = RevisionPlanSerializer(
            data={**request.data, "user": request.user.id}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
def availability_list_create(request):
    if request.method == "GET":
        availabilities = Availability.objects.filter(
            user=request.user
        )

        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = AvailabilitySerializer(
            data={**request.data, "user": request.user.id}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
def revision_session_list_create(request):
    if request.method == "GET":
        sessions = RevisionSession.objects.filter(
            user=request.user
        ).order_by("-date")

        serializer = RevisionSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = RevisionSessionSerializer(
            data={**request.data, "user": request.user.id}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)