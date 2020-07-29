from django.contrib import admin
from questionnaire.models import Questionnaire, Question, Answer

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
   list_display = ['name','date_start','date_end','description',]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
   list_display = ['questionnaire_id','text','type_question',]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
   list_display = ['question_id','text',]