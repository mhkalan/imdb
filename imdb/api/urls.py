from django.urls import path, include
from imdb.api.views import *

urlpatterns = [
    path('', ContentListView.as_view(), name='movie-list'),
    path('content/<int:pk>', ContentDetailView.as_view(), name='movie-detail'),
    path('content/<int:pk>/review', ReviewList.as_view(), name='review-list'),
    path('content/review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('content/<int:pk>/reviewCreate', ReviewCreate.as_view(), name='review-create'),
    path('content/reviews', UserReview.as_view(), name='review-user'),
    path('search', SearchContent.as_view(), name='search'),
    path('order', OrderContent.as_view(), name='order'),
]



