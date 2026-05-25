from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["DELETE"])
def delete_deck(request, deck_id):
    try:
        deck = Deck.objects.get(id=deck_id)
        deck.delete()

        return Response(
            {"message": "Deck supprimé"},
            status=status.HTTP_200_OK,
        )

    except Deck.DoesNotExist:
        return Response(
            {"error": "Deck introuvable"},
            status=status.HTTP_404_NOT_FOUND,
        )