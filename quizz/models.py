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

    def __str__(self):
        return self.title



class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, default="")
    point_value = models.PositiveIntegerField(default=0)
    time_limit_seconds = models.PositiveIntegerField(default=0)  # Add time_limit_seconds field

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the Question model first

        # Update the Quiz fields based on questions after saving
        quiz = self.quiz
        quiz.has_time_limit = any(q.time_limit_seconds > 0 for q in quiz.question_set.all())
        quiz.time_limit_seconds = sum(q.time_limit_seconds for q in quiz.question_set.all())
        quiz.save()  # Save the Quiz model after updating its fields



class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s attempt at {self.quiz.title}"
