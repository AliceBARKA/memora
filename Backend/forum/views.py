from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import ForumPost, ForumComment
from .serializers import ForumPostSerializer, ForumCommentSerializer


def get_current_user(request):
    if request.user and request.user.is_authenticated:
        return request.user

    user = User.objects.first()
    if user is None:
        user = User.objects.create_user(username="default_user", password="password")

    return user


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def forum_post_list_create(request):
    user = get_current_user(request)

    if request.method == "GET":
        posts = ForumPost.objects.all().order_by("-created_at")
        serializer = ForumPostSerializer(posts, many=True)
        return Response(serializer.data)

    serializer = ForumPostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def forum_post_detail(request, post_id):
    user = get_current_user(request)
    post = get_object_or_404(ForumPost, id=post_id)

    if request.method == "GET":
        serializer = ForumPostSerializer(post)
        return Response(serializer.data)

    if request.method == "PATCH":
        if post.author != user and not user.is_superuser:
            return Response(
                {"error": "Tu ne peux modifier que tes propres publications."},
                status=403
            )

        serializer = ForumPostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if post.author != user and not user.is_superuser:
        return Response(
            {"error": "Tu ne peux supprimer que tes propres publications."},
            status=403
        )

    post.delete()
    return Response({"message": "Publication supprimée avec succès."})


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def forum_comment_list_create(request, post_id):
    user = get_current_user(request)
    post = get_object_or_404(ForumPost, id=post_id)

    if request.method == "GET":
        comments = ForumComment.objects.filter(post=post).order_by("created_at")
        serializer = ForumCommentSerializer(comments, many=True)
        return Response(serializer.data)

    serializer = ForumCommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(author=user, post=post)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)