from django.urls import path

from . import views
from . import apiviews

urlpatterns = [
    # path("", views.index, name="index"),
    # path("questions/", apiviews.questions_view, name="questions_view"),
    # path(
    #     "questions/<int:question_id>/",
    #     apiviews.question_detail_view,
    #     name="question_detail_view",
    # ),
    path(
        "questions/<int:question_id>/choices/",
        apiviews.choices_view,
        name="choices_view",
    ),
    path("questions/<int:question_id>/vote/", apiviews.vote_view, name="vote_view"),
    path(
        "questions/<int:question_id>/result/",
        apiviews.question_result_view,
        name="question_result_view",
    ),
    path(
        "multiple-questions/",
        apiviews.multiple_questions_view,
        name="multiple_questions_view",
    ),
    path("questions/", apiviews.QuestionsView.as_view(), name="questions_view"),
    path(
        "questions/<int:question_id>/",
        apiviews.QuestionDetailView.as_view(),
        name="question_detail_view",
    ),
    path(
        "questions/<str:question_text>/",
        apiviews.QuestionDetailView.as_view(),
        name="question_detail_view",
    ),
]
