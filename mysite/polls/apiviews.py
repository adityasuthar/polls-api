from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Question
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Choice
from .serializers import (
    QuestionListPageSerializer,
    ChoiceSerializer,
    VoteSerializer,
    QuestionResultPageSerializer,
    QuestionDetailPageSerializer,
)
import json
from django.shortcuts import get_object_or_404


@api_view(["GET", "POST"])
def questions_view(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionListPageSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = QuestionListPageSerializer(data=request.data)
        if serializer.is_valid():
            # question_text = request.data["question_text"]
            # pub_date = datetime.strptime(request.data["pub_date"], "%Y-%m-%d")
            # Question.objects.create(question_text=question_text, pub_date=pub_date)
            # return HttpResponse("Question created", status=201)
            question = serializer.save()
            return Response(
                QuestionDetailPageSerializer(question).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def multiple_questions_view(request):
    serializer = QuestionListPageSerializer(many=True, data=request.data)
    if serializer.is_valid():
        questions = serializer.save()
        return Response(
            QuestionDetailPageSerializer(questions, many=True).data,
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
def question_detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "GET":
        serializer = QuestionDetailPageSerializer(question)
        return Response(serializer.data)
    elif request.method == "PATCH":
        serializer = QuestionDetailPageSerializer(
            question, data=request.data, partial=True
        )
        if serializer.is_valid():
            return Response(QuestionDetailPageSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def choices_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        choice = serializer.save(question=question)
        return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        choice = get_object_or_404(
            Choice, pk=serializer.validated_data["choice_id"], question=question
        )
        choice.votes += 1
        choice.save()
        return Response("Voted")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def question_result_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = QuestionResultPageSerializer(question)
    return Response(serializer.data)


# @csrf_exempt
# def questions_view(request):
# if 'question_text' not in request.POST or 'pub_date' not in request.POST:
#     return HttpResponse("question_text or pub_date missing", status=400)
#     if request.method == "GET":
#         return HttpResponse("Not Implemented")
#     elif request.method == "POST":
#         question_text = request.POST["question_text"]
#         pub_date = datetime.strptime(request.POST["pub_date"], "%Y-%m-%d")
#         Question.objects.create(question_text=question_text, pub_date=pub_date)
#         return HttpResponse("Question Created", status=201)
