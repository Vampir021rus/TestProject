from django.db import models
from django.contrib.auth.models import User

class UserToken(models.Model):
    user = models.ForeignKey(User, max_length=300, verbose_name="ФИО", null=True, blank=True, on_delete=models.CASCADE)
    token = models.CharField(verbose_name = 'Токе', max_length = 200)


class Questionnaire(models.Model):
    name = models.CharField(verbose_name = 'Название', max_length = 200)
    date_start = models.DateTimeField(verbose_name='Дата начала')
    date_end = models.DateTimeField(verbose_name='Дата Окончания')
    description = models.TextField(verbose_name='Содержание', max_length = 1024)
    
    class Meta:
        verbose_name = 'Опросник'
        verbose_name_plural = 'Опросники'

    def __str__(self):
        return self.name


TYPE_QUESTION = [
    ('text', 'text'),
    ('one', 'one'),
    ('several', 'several'),
]
class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, verbose_name = 'ID опроса', on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(verbose_name = 'Текст вопроса', max_length = 200)
    type_question = models.CharField(max_length = 10, choices=TYPE_QUESTION, default='text')
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(verbose_name = 'Ответ', max_length=300)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.text


class Result(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='results')
    user = models.ForeignKey(User, max_length=300, verbose_name="ФИО", null=True, blank=True, on_delete=models.CASCADE)
    input_text = models.CharField(verbose_name='Ответ текстовый', max_length=300)
    selected = models.ManyToManyField(to=Answer, verbose_name = 'Выбранные ответы')
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'