from django.urls import path
from . import views

urlpatterns = [
    path('api/transcribe/', views.transcribe_audio, name='transcribe_audio'),
    path('api/suggest-titles/', views.suggest_titles, name='suggest_titles'),
] 