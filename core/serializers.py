# serializers.py
from rest_framework import serializers
from .models import FavoriteQuestion, ReadQuestion, Question

class FavoriteQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteQuestion
        fields = '__all__'

class ReadQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadQuestion
        fields = '__all__'

class UserQuestionCountSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    favorite_question_count = serializers.IntegerField()
    read_question_count = serializers.IntegerField()

class QuestionSerializer(serializers.Serializer):
    class Meta:
        model = Question
        fields = '__all__'