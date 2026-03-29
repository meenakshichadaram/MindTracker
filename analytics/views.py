from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Count, Max, Min
from django.utils import timezone
from datetime import timedelta
from moods.models import MoodEntry

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_summary(request):
    user = request.user

    # Last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    entries = MoodEntry.objects.filter(user=user, logged_at__gte=thirty_days_ago)

    avg_mood = entries.aggregate(avg=Avg('score'))['avg']
    total_entries = entries.count()

    # Best and worst mood
    best = entries.order_by('-score').first()
    worst = entries.order_by('score').first()

    # Daily average for chart
    daily = (
        entries
        .values('logged_at__date')
        .annotate(avg_score=Avg('score'), count=Count('id'))
        .order_by('logged_at__date')
    )

    # Streak calculation
    streak = calculate_streak(user)

    return Response({
        'avg_mood': round(avg_mood, 1) if avg_mood else None,
        'total_entries': total_entries,
        'best_mood': {'score': best.score, 'date': best.logged_at} if best else None,
        'worst_mood': {'score': worst.score, 'date': worst.logged_at} if worst else None,
        'daily_chart': list(daily),
        'current_streak': streak['current'],
        'longest_streak': streak['longest'],
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_report(request):
    user = request.user
    today = timezone.now().date()
    reports = []

    # Generate last 4 weeks report
    for week in range(4):
        # Calculate week start and end
        week_end = today - timedelta(days=week * 7)
        week_start = week_end - timedelta(days=6)

        # Get all entries for that week
        entries = MoodEntry.objects.filter(
            user=user,
            logged_at__date__gte=week_start,
            logged_at__date__lte=week_end
        )

        if entries.exists():
            # Calculate stats
            avg = entries.aggregate(avg=Avg('score'))['avg']
            total = entries.count()

            # Best and worst day
            best = entries.order_by('-score').first()
            worst = entries.order_by('score').first()

            # Most used tag
            tags = {}
            for entry in entries:
                for tag in entry.tags.all():
                    tags[tag.name] = tags.get(tag.name, 0) + 1
            most_used_tag = max(tags, key=tags.get) if tags else None

            # Mood trend - compare first half vs second half of week
            mid = week_start + timedelta(days=3)
            first_half = entries.filter(logged_at__date__lte=mid).aggregate(avg=Avg('score'))['avg']
            second_half = entries.filter(logged_at__date__gt=mid).aggregate(avg=Avg('score'))['avg']

            if first_half and second_half:
                if second_half > first_half:
                    trend = 'improving'
                elif second_half < first_half:
                    trend = 'declining'
                else:
                    trend = 'stable'
            else:
                trend = 'stable'

            reports.append({
                'week': f'Week of {week_start}',
                'week_start': week_start,
                'week_end': week_end,
                'avg_mood': round(avg, 1),
                'total_entries': total,
                'best_mood': {'score': best.score, 'date': best.logged_at},
                'worst_mood': {'score': worst.score, 'date': worst.logged_at},
                'most_used_tag': most_used_tag,
                'trend': trend,
            })
        else:
            reports.append({
                'week': f'Week of {week_start}',
                'week_start': week_start,
                'week_end': week_end,
                'avg_mood': None,
                'total_entries': 0,
                'best_mood': None,
                'worst_mood': None,
                'most_used_tag': None,
                'trend': 'no data',
            })

    return Response(reports)


def calculate_streak(user):
    # Get all unique dates user logged a mood, newest first
    dates = (
        MoodEntry.objects
        .filter(user=user)
        .values_list('logged_at__date', flat=True)
        .distinct()
        .order_by('-logged_at__date')
    )

    dates = list(dates)

    if not dates:
        return {'current': 0, 'longest': 0}

    # Current streak
    current_streak = 0
    today = timezone.now().date()
    expected = today

    for date in dates:
        if date == expected:
            current_streak += 1
            expected -= timedelta(days=1)
        elif date == today - timedelta(days=1) and current_streak == 0:
            current_streak += 1
            expected = date - timedelta(days=1)
        else:
            break

    # Longest streak
    longest_streak = 0
    temp_streak = 1

    for i in range(len(dates) - 1):
        diff = (dates[i] - dates[i + 1]).days
        if diff == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

    longest_streak = max(longest_streak, temp_streak)

    return {'current': current_streak, 'longest': longest_streak}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mood_heatmap(request):
    from moods.models import MoodEntry
    entries = (
        MoodEntry.objects
        .filter(user=request.user)
        .values('logged_at__date')
        .annotate(avg_score=Avg('score'))
        .order_by('logged_at__date')
    )
    data = {
        str(e['logged_at__date']): round(e['avg_score'], 1)
        for e in entries
    }
    return Response(data)