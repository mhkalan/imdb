from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from .permissions import *
from .pagination import *

# Create your views here.


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(author__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-create'

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        content = Content.objects.get(pk=pk)
        author = self.request.user
        author_queryset = Review.objects.filter(content=content, author=author)
        if author_queryset.exists():
            raise ValidationError('You have rated already')

        if content.totalNumberOfRatings == 0:
            content.averageRating = serializer.validated_data['rating']
        else:
            content.averageRating = (content.averageRating + serializer.validated_data['rating']) / 2

        content.totalNumberOfRatings += 1
        content.save()
        serializer.save(content=content, author=author)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-list'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author__username', 'rating', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(content=pk)


class ContentListView(APIView):
    permission_classes = [AdminOrReadOnlY]
    pagination_class = ContentCursorPagination

    def get(self, request):
        movie = Content.objects.all()
        serializer = ContentSerializer(movie, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailView(APIView):
    permission_classes = [AdminOrReadOnlY]

    def get(self, request, pk):
        try:
            movie = Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ContentSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = Content.objects.get(pk=pk)
        serializer = ContentSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = Content.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchContent(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'streamPlatform']


class OrderContent(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['averageRating']


