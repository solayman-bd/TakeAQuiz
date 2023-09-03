from django.urls import path
from . import views

urlpatterns = [
    # path('allquiz/', views.allquiz, name='allquiz'),
    path('takequiz/', views.takequiz, name='takequiz'),
    path('takequiz/<int:category_id>/', views.showquiz, name='showquiz'), 
    path('takequiz/<int:category_id>/<int:quiz_id>', views.startquiz, name='startquiz'),
    path('takequiz/submitquiz',views.quizsubmit,name='quizsubmit'),
     path('leaderboard/', views.leaderboard, name='leaderboard'),
]
