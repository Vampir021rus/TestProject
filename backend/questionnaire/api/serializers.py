from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models import Questionnaire, Question, Answer, Result, UserToken


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Questionnaire
        fields='__all__'
    
    def create(self, validated_data):
        return Questionnaire.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        #instance.date_start = validated_data.get('date_start', instance.date_start) дату старта не обновляем
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Question
        fields='__all__'
    
    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.questionnaire = validated_data.get('questionnaire', instance.questionnaire)
        instance.text = validated_data.get('text', instance.text)
        instance.type_question = validated_data.get('type_question', instance.type_question)
        instance.save()
        return instance


class AnswerSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Answer
        fields='__all__'
    
    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class ResultSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Result
        fields='__all__'
    
    def create(self, validated_data):
        return Result.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.user = validated_data.get('user', instance.user)
        instance.input_text = validated_data.get('input_text', instance.input_text)
        instance.selected = validated_data.get('selected', instance.selected)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta: 
        model=User
        fields = (
            'username',
            'password',
        )

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username:
            raise serializers.ValidationError('An name is required to login.')

        if not password:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')
        
        token, _ = Token.objects.get_or_create(user=user)

        return {
            'token': token.key,
        }
