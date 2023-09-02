from django.contrib import admin
from .models import Category, Quiz, Question, Option, QuizAttempt

# Register your models here.
models_to_register = [Category, Quiz, Question, Option, QuizAttempt]

for model in models_to_register:
    admin.site.register(model)
