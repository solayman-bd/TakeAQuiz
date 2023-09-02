from django.urls import path
from . import views
urlpatterns = [
     path('allquiz/', views.allquiz, name = 'allquiz'),
    path('allquiz/', views.allquiz, name = 'allquiz'),
]
