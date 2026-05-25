from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    name = request.data.get("name")

    if not username or not password:
        return Response({"error": "Champs manquants"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Utilisateur déjà existe"}, status=400)

    user = User.objects.create_user(
    username=username,
    first_name=name,
    password=password
)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "name": user.first_name,
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Identifiants incorrects"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "name": user.first_name,
    })