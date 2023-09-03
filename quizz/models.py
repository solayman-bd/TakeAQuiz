from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    has_time_limit = models.BooleanField(default=False)
    time_limit_seconds = models.PositiveIntegerField(default=0)
    total_marks=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title



class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, default="")
    point_value = models.PositiveIntegerField(default=0)
    time_limit_seconds = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        quiz = self.quiz
        quiz.has_time_limit = any(q.time_limit_seconds > 0 for q in quiz.question_set.all())
        quiz.time_limit_seconds = sum(q.time_limit_seconds for q in quiz.question_set.all())
        quiz.total_marks=sum(q.point_value for q in quiz.question_set.all())
        quiz.save()



class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total_limit_seconds = models.IntegerField(default=0)
    completion_time = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s attempt at {self.quiz.title}"
    
class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total_score = models.PositiveIntegerField(default=0)
    taken_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s top score in {self.quiz.title}"