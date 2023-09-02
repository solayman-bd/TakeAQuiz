from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Quiz, Question, Option, QuizAttempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


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

@login_required(login_url='login')
def takequiz(request):
    categories = Category.objects.all()
    user = request.user
    return render(request, 'quizz/takequiz.html', {'categories': categories,'user':user})

@login_required(login_url='login')
def showquiz(request, category_id):
    # Filter quizzes based on the provided category_id
    quizzes = Quiz.objects.filter(category__id=category_id)
    user = request.user
    # Pass the quizzes queryset to the template
    return render(request, 'quizz/showquiz.html', {'quizzes': quizzes, 'user':user, 'category_id': category_id})

@login_required(login_url='login')
def startquiz(request, category_id, quiz_id):
    # Filter questions based on the provided quiz_id
    selected_quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz__id=quiz_id)
    user = request.user
    quiz_time=0
    if selected_quiz.has_time_limit==True:
        quiz_time=selected_quiz.time_limit_seconds
    # Pass the questions queryset to the template
    return render(request, 'quizz/startquiz.html', {'questions': questions, 'user': user,'quiz_time':quiz_time, 'quiz':selected_quiz})


@login_required(login_url='login')
def quizsubmit(request):
    if request.method=="POST":
        submission_data={
            "marks":request.POST["marks"],
            "selected_quiz":request.POST["selected_quiz"],
            "total_time":request.POST["total_time"],
            "completion_time":request.POST["completion_time"]
        }
        print("Completion Time:",request.POST["completion_time"])
        print("Marks:",request.POST["marks"])    
        print("Total Time:",request.POST["total_time"])
        print("Selected Quiz:",request.POST["selected_quiz"])
    return render(request, 'quizz/quizsubmit.html', )
