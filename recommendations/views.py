from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Recommendation
from .serializers import RecommendationSerializer
from django.db.models import Avg
from moods.models import MoodEntry

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendation_list(request):
    # Auto generate recommendation based on recent mood average
    recent_moods = MoodEntry.objects.filter(user=request.user).order_by('-logged_at')[:7]
    if recent_moods.exists():
        avg = recent_moods.aggregate(avg=Avg('score'))['avg']
        if avg <= 4:
            title = 'Try a breathing exercise'
            content = 'Your mood has been low lately. Try 5 minutes of deep breathing.'
            category = 'mindfulness'
        elif avg <= 6:
            title = 'Go for a short walk'
            content = 'A 15 minute walk can boost your mood significantly.'
            category = 'exercise'
        else:
            title = 'Keep it up!'
            content = 'Your mood is great. Keep doing what you are doing.'
            category = 'general'

        Recommendation.objects.get_or_create(
            user=request.user,
            title=title,
            defaults={'content': content, 'category': category}
        )

    recommendations = Recommendation.objects.filter(user=request.user).order_by('-generated_at')
    serializer = RecommendationSerializer(recommendations, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_read(request, id):
    try:
        rec = Recommendation.objects.get(id=id, user=request.user)
    except Recommendation.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    rec.is_read = True
    rec.save()
    return Response({'message': 'Marked as read'})