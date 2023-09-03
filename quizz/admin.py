from django.contrib import admin
from .models import Category, Quiz, Question, Option, QuizAttempt,QuizRating

# Register your models here.
models_to_register = [Category,  Question, Option, QuizAttempt,QuizRating, Quiz]

for model in models_to_register:
    admin.site.register(model)
