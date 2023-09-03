from django.shortcuts import render, redirect
from .models import Category, Quiz, Question, Option, QuizAttempt,QuizRating
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# def allquiz(request):
#     if request.method == "GET":
#         categories = Category.objects.all()
#         data = []

#         for category in categories:
#             category_data = {
#                 'category_name': category.name,
#                 'quizzes': []
#             }

#             quizzes = Quiz.objects.filter(category=category)

#             for quiz in quizzes:
#                 quiz_data = {
#                     'quiz_title': quiz.title,
#                     'has_time_limit':quiz.has_time_limit,
#                     'time_limit_in_seconds':quiz.time_limit_seconds,
#                     'questions': []
#                 }

#                 questions = Question.objects.filter(quiz=quiz)

#                 for question in questions:
#                     question_data = {
#                         'question_text': question.text,
#                         'time_limit_in_seconds':question.time_limit_seconds,
#                         'options': []
#                     }

#                     options = Option.objects.filter(question=question)

#                     for option in options:
#                         question_data['options'].append({
#                             'option_text': option.text,
#                             'is_correct': option.is_correct
#                         })

#                     quiz_data['questions'].append(question_data)

#                 category_data['quizzes'].append(quiz_data)

#             data.append(category_data)

#         return JsonResponse({'data': data})
#     else:
#         return HttpResponse("Hello, world.")

@login_required(login_url='login')
def takequiz(request):
    categories = Category.objects.all()
    user = request.user
    return render(request, 'quizz/takequiz.html', {'categories': categories,'user':user})

@login_required(login_url='login')
def showquiz(request, category_id):
  
    quizzes = Quiz.objects.filter(category__id=category_id)
    user = request.user
 
    return render(request, 'quizz/showquiz.html', {'quizzes': quizzes, 'user':user, 'category_id': category_id})

@login_required(login_url='login')
def startquiz(request, category_id, quiz_id):

    selected_quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz__id=quiz_id)
    user = request.user
    quiz_time=0
    if selected_quiz.has_time_limit==True:
        quiz_time=selected_quiz.time_limit_seconds
    return render(request, 'quizz/startquiz.html', {'questions': questions, 'user': user,'quiz_time':quiz_time, 'quiz':selected_quiz})


@login_required(login_url='login')
def quizsubmit(request):
    if request.method == "POST":
        quiz_id=request.POST["selected_quiz"]
        user = request.user
        quiz = get_object_or_404(Quiz, id=quiz_id)
        rating=False
        rating_ins=QuizRating.objects.filter(user=user,quiz=quiz)
        if  rating_ins.exists():
            rating=rating_ins[0]
        time_limit_seconds = request.POST["total_time"]
        completion_time = request.POST["completion_time"]
        score = request.POST["marks"]
        quiz_attempt = QuizAttempt(
            user=user,
            quiz=quiz,
            total_limit_seconds=time_limit_seconds,
            completion_time=completion_time,
            score=score,
        )
        quiz_attempt.save()
        submission_data = {
            "marks": score,
            "quiz": quiz,
            "total_time": time_limit_seconds,
            "completion_time": completion_time,
            'rating':rating
        }
        
        return render(request, 'quizz/quizsubmit.html', {"submission_data": submission_data, "user": user})
    else:
        return redirect('login')
    

@login_required(login_url='login')
def quizrating(request):
    if request.method == "POST":
        user = request.user
        quiz_id = request.POST["quiz"]
        quiz = get_object_or_404(Quiz, id=quiz_id)
        rating = request.POST["rating"]
        quiz_rating = QuizRating(
            user=user,
            quiz=quiz,
            rating=rating
        )
        quiz_rating.save()
        return render(request, 'quizz/success.html', {'user': user, 'quiz': quiz, 'rating': rating})
    else:
        return redirect('home')

@login_required(login_url='login')
def leaderboard(request):
    top_attempts = QuizAttempt.objects.filter(score__isnull=False).order_by('-score')[:10]
    return render(request, 'quizz/leaderboard.html', {'top_attempts': top_attempts})
