from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import views
import os

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'activities', views.ActivityViewSet, basename='activity')
router.register(r'leaderboard', views.LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', views.WorkoutViewSet, basename='workout')

# Custom API root view with Codespace URL support
@api_view(['GET'])
def api_root_codespace(request, format=None):
    """
    API root endpoint that provides links to all available endpoints.
    Uses Codespace URL if available, otherwise falls back to request host.
    """
    codespace_name = os.environ.get('CODESPACE_NAME')
    
    if codespace_name:
        # Use Codespace URL
        base_url = f'https://{codespace_name}-8000.app.github.dev/api'
    else:
        # Fallback to request host
        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        base_url = f'{scheme}://{host}/api'
    
    return Response({
        'users': f'{base_url}/users/',
        'teams': f'{base_url}/teams/',
        'activities': f'{base_url}/activities/',
        'leaderboard': f'{base_url}/leaderboard/',
        'workouts': f'{base_url}/workouts/',
    })

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', api_root_codespace, name='api_root'),
    path('', include(router.urls)),
]
