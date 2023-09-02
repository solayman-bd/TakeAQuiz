from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Quiz, Question, Option, QuizAttempt
from django.http import JsonResponse

def allquiz(request):
    if request.method == "GET":
        categories = Category.objects.all()
        data = []

        for category in categories:
            category_data = {
                'category_name': category.name,
                'quizzes': []
            }

            quizzes = Quiz.objects.filter(category=category)

            for quiz in quizzes:
                quiz_data = {
                    'quiz_title': quiz.title,
                    'has_time_limit':quiz.has_time_limit,
                    'time_limit_in_seconds':quiz.time_limit_seconds,
                    'questions': []
                }

                questions = Question.objects.filter(quiz=quiz)

                for question in questions:
                    question_data = {
                        'question_text': question.text,
                        'time_limit_in_seconds':question.time_limit_seconds,
                        'options': []
                    }

                    options = Option.objects.filter(question=question)

                    for option in options:
                        question_data['options'].append({
                            'option_text': option.text,
                            'is_correct': option.is_correct
                        })

                    quiz_data['questions'].append(question_data)

                category_data['quizzes'].append(quiz_data)

            data.append(category_data)

        return JsonResponse({'data': data})
    else:
        return HttpResponse("Hello, world. You're at the polls index.")
