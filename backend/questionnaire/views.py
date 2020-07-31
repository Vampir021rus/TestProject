import json
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from questionnaire.api.serializers import LoginSerializer, QuestionnaireSerializer, QuestionSerializer, AnswerSerializer, ResultSerializer
from .models import Questionnaire, Question, Answer, Result

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionnaireListView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionnaireSerializer

    def get(self, request):
        qs = Questionnaire.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = json.loads(request.body)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionnaireDetailView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionnaireSerializer

    def get_object(self, pk):
        try:
            return Questionnaire.objects.get(pk=pk)
        except Questionnaire.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        questionnaire = self.get_object(pk)
        serializer = self.serializer_class(questionnaire)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        questionnaire = self.get_object(pk)
        serializer = self.serializer_class(questionnaire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        questionnaire = self.get_object(pk)
        questionnaire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionListView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionSerializer

    def get(self, request, pk, format=None):
        qs = Question.objects.filter(questionnaire=pk)
        data = []
        for question in qs:
            serializer = self.serializer_class(question)
            data.append(serializer.data)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        data = json.loads(request.body)
        data['questionnaire']=pk
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionSerializer

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, pk_quest, format=None):
        question = self.get_object(pk_quest)
        serializer = self.serializer_class(question)
        return Response(serializer.data)

    def put(self, request, pk, pk_quest, format=None):
        question = self.get_object(pk_quest)
        data=request.data        
        print(data)
        serializer = self.serializer_class(question, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, pk_quest, format=None):
        question = self.get_object(pk_quest)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerListView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = AnswerSerializer

    def get(self, request, pk,pk_quest, format=None):
        qs = Answer.objects.filter(question=pk_quest)
        data = []
        for question in qs:
            serializer = self.serializer_class(question)
            data.append(serializer.data)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk, pk_quest, format=None):
        data = json.loads(request.body)
        data['question']=pk_quest
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetailView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = AnswerSerializer

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk, pk_quest, pk_answer, format=None):
        answer = self.get_object(pk_answer)
        serializer = self.serializer_class(answer)
        return Response(serializer.data)

    def put(self, request, pk, pk_quest, pk_answer, format=None):
        answer = self.get_object(pk_answer)
        serializer = self.serializer_class(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, pk_quest, pk_answer, format=None):
        answer = self.get_object(pk_answer)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionnaireActiveListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionnaireSerializer

    def get(self, request):
        dt = datetime.now()
        qs = Questionnaire.objects.filter(date_start__lt=dt, date_end__gt=dt)
        data = []
        for questionnaire in qs:
            serializer = self.serializer_class(questionnaire)
            data.append(serializer.data)
        return Response(data, status=status.HTTP_200_OK)