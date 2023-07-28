from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import User, Question, FavoriteQuestion, ReadQuestion
from .serializers import FavoriteQuestionSerializer, ReadQuestionSerializer, UserQuestionCountSerializer, QuestionSerializer
from rest_framework import filters
from django.core.cache import cache

class FavoriteQuestionViewSet(viewsets.ModelViewSet):
    queryset = FavoriteQuestion.objects.all()
    serializer_class = FavoriteQuestionSerializer

class ReadQuestionViewSet(viewsets.ModelViewSet):
    queryset = ReadQuestion.objects.all()
    serializer_class = ReadQuestionSerializer

class UserQuestionCountPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserQuestionCountView(ListAPIView):

    serializer_class = UserQuestionCountSerializer
    pagination_class = UserQuestionCountPagination

    def get_queryset(self):
        # Try to fetch data from the cache
        cached_data = cache.get('user_question_count')
        if cached_data is not None:
            return cached_data

        users = User.objects.all()
        queryset = []
        for user in users:
            favorite_count = user.fav_question_user_set.count()
            read_count = user.read_question_user_set.count()
            queryset.append({
                'user_id': user.id,
                'favorite_question_count': favorite_count,
                'read_question_count': read_count,
            })
        # Store the data in cache for 5 minutes (300 seconds)
        cache.set('user_question_count', queryset, 300)

        return queryset
    
class QuestionFilterView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        # Try to fetch data from the cache
        cached_data = cache.get('filter_data')
        if cached_data is not None:
            return cached_data

        status = self.request.query_params.get('status', None)
        if status == 'read':
            return self.queryset.filter(read_by__isnull=False).distinct()
        elif status == 'unread':
            return self.queryset.filter(read_by__isnull=True)
        elif status == 'favorite':
            return self.queryset.filter(favorite_by__isnull=False).distinct()
        elif status == 'unfavorite':
            return self.queryset.filter(favorite_by__isnull=True)
        
        # Store the data in cache for 5 minutes (300 seconds)
        cache.set('filter_data', self.queryset, 300)
        return self.queryset


