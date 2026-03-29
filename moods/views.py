from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import MoodEntry, Tag
from .serializers import MoodEntrySerializer, TagSerializer
import random

LOW_MOOD_QUOTES = [
    "Every storm runs out of rain. Keep going 💙",
    "You are stronger than you think. One day at a time 🌱",
    "It's okay to not be okay. Tomorrow is a new chance 🌅",
    "Hard times never last. You got this 💪",
    "Be gentle with yourself. You are doing the best you can 🤍",
    "Even the darkest night will end and the sun will rise 🌄",
    "You have survived 100% of your worst days so far 🔥",
    "Small steps still move you forward. Keep walking 👣",
]

MID_MOOD_QUOTES = [
    "You are making progress even when it doesn't feel like it 🌿",
    "Balance is not something you find, it's something you create ⚖️",
    "Steady and consistent beats fast and burned out 🐢",
    "Every day is a fresh start. Make it count 🌤️",
    "You are exactly where you need to be right now 🧭",
    "Small joys add up to a beautiful life 🌸",
]

HIGH_MOOD_QUOTES = [
    "You are absolutely crushing it! Keep shining ⭐",
    "This energy is contagious! Spread the good vibes 🌟",
    "Amazing days like this are worth celebrating 🎉",
    "You are at your best — remember this feeling 💫",
    "Happiness looks great on you! Keep it up 😊",
    "You are glowing today! The world needs your energy 🌞",
    "Ride this wave and enjoy every moment 🏄",
]

def get_quote(score):
    if score <= 4:
        return random.choice(LOW_MOOD_QUOTES)
    elif score <= 7:
        return random.choice(MID_MOOD_QUOTES)
    else:
        return random.choice(HIGH_MOOD_QUOTES)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mood_list(request):
    if request.method == 'GET':
        moods = MoodEntry.objects.filter(user=request.user)

        score = request.query_params.get('score')
        if score:
            moods = moods.filter(score=score)

        ordering = request.query_params.get('ordering')
        if ordering:
            moods = moods.order_by(ordering)

        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_moods = paginator.paginate_queryset(moods, request)
        serializer = MoodEntrySerializer(paginated_moods, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        serializer = MoodEntrySerializer(data=request.data)
        if serializer.is_valid():
            entry = serializer.save(user=request.user)
            quote = get_quote(entry.score)
            data = serializer.data
            data['quote'] = quote
            return Response(data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def mood_detail(request, id):
    try:
        mood = MoodEntry.objects.get(id=id, user=request.user)
    except MoodEntry.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        serializer = MoodEntrySerializer(mood)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = MoodEntrySerializer(mood, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'PATCH':
        serializer = MoodEntrySerializer(mood, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        mood.delete()
        return Response({'message': 'Mood entry deleted'}, status=204)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tag_list(request):
    if request.method == 'GET':
        tags = Tag.objects.filter(user=request.user)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)