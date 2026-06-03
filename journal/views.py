from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import JournalEntry
from .serializers import JournalEntrySerializer, PublicJournalEntrySerializer
from .permissions import IsOwnerOrEditorReadOnly

class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrEditorReadOnly]

    def get_queryset(self):
        # Se o usuário está no grupo 'Editor', pode ver todas as entradas
        if self.request.user.groups.filter(name='Editor').exists():
            return JournalEntry.objects.all()
        # Caso contrário, vê apenas suas próprias entradas
        return JournalEntry.objects.filter(author=self.request.user)

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)


class PublicJournalEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JournalEntry.objects.filter(is_public=True)
    serializer_class = PublicJournalEntrySerializer
    permission_classes = [AllowAny]
