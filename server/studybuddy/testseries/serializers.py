from rest_framework import serializers
from .models import Subject, Subdomain, Chapter, Question, Test, Answer

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class SubdomainSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Subdomain
        fields = ['id', 'name', 'subject']

class ChapterSerializer(serializers.ModelSerializer):
    subdomain = SubdomainSerializer()

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'subdomain']

class QuestionSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer()
    
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'text_image', 'option1', 'option2', 'option3', 'option4',
            'option1_image', 'option2_image', 'option3_image', 'option4_image',
            'correct_option', 'marks', 'negative_marks', 'chapter'
        ]

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    shared_with = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        model = Test
        fields = ['id', 'user', 'name', 'created_at', 'duration', 'questions', 'score']

class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ['id', 'test', 'question', 'selected_option', 'correct']

class TestDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'user', 'name', 'created_at', 'duration', 'score', 'questions', 'answers']