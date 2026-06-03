from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import RegisterView, CurrentUserView, LogoutView
from journal.views import JournalEntryViewSet, PublicJournalEntryViewSet

# Gerador automático de URLs para o CRUD do Diário
router = DefaultRouter()
router.register(r'entries', JournalEntryViewSet, basename='journalentry')
router.register(r'journal/public', PublicJournalEntryViewSet, basename='public_journalentry')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Endpoints de Autenticação e Emissão de Tokens
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', CurrentUserView.as_view(), name='current_user'),
    path('api/auth/logout/', LogoutView.as_view(), name='auth_logout'),
    
    # Endpoints do Recurso Protegido e Públicos (/api/entries/ e /api/journal/public/)
    path('api/', include(router.urls)),
]