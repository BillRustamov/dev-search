from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('profiles', views.ProfileViewSet)

urlpatterns = [
    path('projects/', views.get_projects),
    path('projects/<str:pk>/', views.get_project),

    # http://localhost:8000/api/tags/create/
    path('tags/create/', views.create_tag),
    
    # http://localhost:8000/api/tags/delete/
    path('tags/delete/', views.delete_tag),
] + router.urls
