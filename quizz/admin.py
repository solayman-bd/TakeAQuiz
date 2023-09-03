from django.contrib import admin
from .models import Category, Quiz, Question, Option, QuizAttempt,QuizRating

# Register your models here.
models_to_register = [Category, Quiz, Question, Option, QuizAttempt,QuizRating]

for model in models_to_register:
    admin.site.register(model)
