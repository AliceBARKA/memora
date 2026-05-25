from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ToDo
from .serializers import ToDoSerializer


@api_view(["GET", "POST"])
def todo_list_create(request):
    if request.method == "GET":
        todos = ToDo.objects.filter(
    user=request.user
)
        serializer = ToDoSerializer(todos, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        user = request.user

        serializer = ToDoSerializer(
            data={**request.data, "user": user.id}
    )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(["PATCH", "DELETE"])
def todo_detail(request, todo_id):
    try:
        todo = ToDo.objects.get(
    id=todo_id,
    user=request.user
)
    except ToDo.DoesNotExist:
        return Response({"error": "Todo introuvable"}, status=404)

    if request.method == "PATCH":
        serializer = ToDoSerializer(todo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        todo.delete()
        return Response({"message": "Todo supprimée"})
