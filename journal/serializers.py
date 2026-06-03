from rest_framework import serializers
from .models import JournalEntry

class JournalEntrySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = JournalEntry
        fields = ['id', 'author', 'title', 'content', 'mood', 'is_public', 'created_at']


class PublicJournalEntrySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = JournalEntry
        fields = ['id', 'author', 'title', 'content', 'mood', 'created_at']