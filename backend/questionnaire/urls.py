from django.urls import path
from . import views

urlpatterns = [ 
    path('login', views.LoginView.as_view()),

    path('questionnaires', views.QuestionnaireListView.as_view()),
    path('questionnaires/<int:pk>', views.QuestionnaireDetailView.as_view()),

    path('questionnaires/<int:pk_questionnaire>/questions', views.QuestionListView.as_view()),
    path('questionnaires/<int:pk_questionnaire>/questions/<int:pk>', views.QuestionDetailView.as_view()),

    path('questionnaires/<int:pk_questionnaire>/questions/<int:pk_quest>/answers', views.AnswerListView.as_view()),
    path('questionnaires/<int:pk_questionnaire>/questions/<int:pk_quest>/answers/<int:pk>', views.AnswerDetailView.as_view()),

    path('active-questionnaires', views.QuestionnaireActiveListView.as_view()),
    path('results', views.QuestionnaireActiveListView.as_view()),
]
