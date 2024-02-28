
from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views.CP_QuizView import *
router = DefaultRouter()


urlpatterns = [
    # re_path(r'^quizzes$', GetQuizzesAPI.as_view()),
]
