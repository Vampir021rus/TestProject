import json
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from questionnaire.api.serializers import LoginSerializer, QuestionnaireSerializer, QuestionSerializer, AnswerSerializer
from .models import Questionnaire, Question, Answer, Result


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionnaireListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class QuestionnaireDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.all()


class QuestionListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get(self, request, pk_questionnaire, *args, **kwargs):
        self.queryset = self.queryset.filter(questionnaire=pk_questionnaire)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def get(self, request, pk_questionnaire, pk_quest, format=None):
        self.queryset = self.queryset.filter(question=pk_quest)
        return self.list(request, *args, **kwargs)

    def post(self, request, format=None):
        return self.create(request, *args, **kwargs)


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class QuestionnaireActiveListView(ListModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.all()

    def get(self, request):
        dt = datetime.now()
        self.queryset = self.queryset.filter(date_start__lt=dt, date_end__gt=dt)
        return self.list(request, *args, **kwargs)