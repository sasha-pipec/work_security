from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользовватели'


class Gallery(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')

    def __str__(self):
        return str(self.image.name)

    class Meta:
        db_table = 'gallery'
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


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
        verbose_name = 'Инструкция'
        verbose_name_plural = 'Интсрукции'


class Test(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    instruction = models.ForeignKey('Instruction', on_delete=models.CASCADE, verbose_name='Инструкция')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'test'
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    test = models.ForeignKey('Test', on_delete=models.CASCADE, verbose_name='Тест')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'question'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.BooleanField(verbose_name='Ответ')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'answer'
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TestToUser(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    score = models.IntegerField(verbose_name='Оценка')

    def __str__(self):
        return f"{self.test.title} {self.user.username} {self.score}"

    class Meta:
        db_table = 'testtouser'
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
