from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Subject, Subdomain, Chapter, Question, Test, Answer
from .serializers import SubjectSerializer, SubdomainSerializer, ChapterSerializer, QuestionSerializer, TestSerializer, AnswerSerializer,TestSerializer, TestDetailSerializer
from authentication.models import User
import jwt
import random
from django.conf import settings

def get_user_from_token(request):
    try:
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None, {"error": "Authorization header missing"}, status.HTTP_401_UNAUTHORIZED
        
        token = authorization_header.split(' ')[1]
        decoded_token = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        
        user_id = decoded_token.get('id')
        if not user_id:
            return None, {"error": "Invalid token format"}, status.HTTP_403_FORBIDDEN
        
        user = get_object_or_404(User, id=user_id)
        return user, None, None
    except jwt.ExpiredSignatureError:
        return None, {"error": "Token has expired"}, status.HTTP_403_FORBIDDEN
    except jwt.DecodeError:
        return None, {"error": "Invalid token"}, status.HTTP_403_FORBIDDEN
    except Exception as e:
        return None, {"error": str(e)}, status.HTTP_403_FORBIDDEN
@api_view(['GET'])
def get_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_subdomains(request, subject_id):
    subdomains = Subdomain.objects.filter(subject_id=subject_id)
    serializer = SubdomainSerializer(subdomains, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_chapters(request, subdomain_id):
    chapters = Chapter.objects.filter(subdomain_id=subdomain_id)
    serializer = ChapterSerializer(chapters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_questions(request, chapter_ids):
    chapter_ids = chapter_ids.split(',')
    questions = Question.objects.filter(chapter_id__in=chapter_ids)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def generate_test(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)

    chapter_ids = request.data.get('chapter_ids')
    duration = request.data.get('duration')
    
    question_count = 0
    if duration == 15:
        question_count = 5
    elif duration == 30:
        question_count = 10
    elif duration == 60:
        question_count = 20

    questions = Question.objects.filter(chapter_id__in=chapter_ids).order_by('?')[:question_count]

    test = Test.objects.create(user=user, duration=duration)
    test.questions.set(questions)
    test.save()

    serializer = TestSerializer(test)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def submit_test(request, test_id):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)

    test = Test.objects.get(id=test_id)
    answers = request.data.get('answers')

    total_score = 0

    for answer in answers:
        question_id = answer.get('question_id')
        selected_option = answer.get('selected_option')
        question = Question.objects.get(id=question_id)
        correct = (selected_option == question.correct_option)

        if correct:
            total_score += question.marks
        else:
            total_score -= question.negative_marks

        Answer.objects.create(test=test, question=question, selected_option=selected_option, correct=correct)

    test.score = total_score
    test.save()

    return Response({"score": total_score}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_test_result(request, test_id):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)

    test = Test.objects.get(id=test_id)
    answers = Answer.objects.filter(test=test)

    test_serializer = TestSerializer(test)
    answer_serializer = AnswerSerializer(answers, many=True)

    return Response({"test": test_serializer.data, "answers": answer_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_previous_tests(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    tests = Test.objects.filter(user=user)
    serializer = TestSerializer(tests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_test_detail(request, test_id):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    test = get_object_or_404(Test, id=test_id, user=user)
    serializer = TestDetailSerializer(test)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def share_test(request, pk):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)

    test = get_object_or_404(Test, pk=pk)
    if test.user != user:
        return Response({"error": "You do not have permission to share this test."}, status=status.HTTP_403_FORBIDDEN)

    user_ids = request.data.get('user_ids', [])
    users = User.objects.filter(id__in=user_ids)
    test.shared_with.add(*users)

    return Response({"message": "Test shared successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def shared_tests(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)

    tests = Test.objects.filter(shared_with=user)
    serializer = TestSerializer(tests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_test_questions(request, test_id):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)

    test = get_object_or_404(Test, id=test_id, user=user)
    questions = test.questions.all()
    
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
