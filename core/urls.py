from django.urls import path, include
from core.views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'favorite-questions', FavoriteQuestionViewSet, basename='favorite-question')
router.register(r'read-questions', ReadQuestionViewSet, basename='read-question')

urlpatterns = [
    path('', include(router.urls)),
    path('user-data/',
         UserQuestionCountView.as_view(), name='user-data'),
    path('question-filter/',
         QuestionFilterView.as_view(), name='question-filter'),
]