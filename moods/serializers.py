from rest_framework import serializers
from .models import MoodEntry, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['user']  # add this line

class MoodEntrySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, source='tags', required=False
    )

    class Meta:
        model = MoodEntry
        fields = ['id', 'user', 'score', 'note', 'tags', 'tag_ids',
                  'sleep_hours', 'energy_level', 'logged_at']
        read_only_fields = ['user', 'logged_at']