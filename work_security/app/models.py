from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    pass


class Gallery(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')

    def __str__(self):
        return str(self.image.name)

    class Meta:
        db_table = 'gallery'
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'


class Instruction(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    short_description = models.TextField(max_length=500, verbose_name='Краткое описание')
    gallery = models.ManyToManyField('Gallery', verbose_name='Галерея ')
    file = models.FileField(upload_to='files/', verbose_name='Файл инструкции')
    created_at = models.DateField(null=True, auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'instruction'
        verbose_name = 'Instruction'
        verbose_name_plural = 'Instructions'


class Test(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    instruction = models.ForeignKey('Instruction', on_delete=models.CASCADE, verbose_name='Инструкция')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'test'
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    test = models.ForeignKey('Test', on_delete=models.CASCADE, verbose_name='Тест')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'question'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.BooleanField(verbose_name='Ответ')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'answer'
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class TestToUser(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    score = models.IntegerField(verbose_name='Оценка')

    def __str__(self):
        return f"{self.test.title} {self.user.username} {self.score}"

    class Meta:
        db_table = 'testtouser'
        verbose_name = 'TestToUser'
        verbose_name_plural = 'TestToUsers'
