# Generated by Django 4.2.4 on 2023-09-03 15:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizz', '0002_leaderboard'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizz.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'quiz')},
            },
        ),
    ]
