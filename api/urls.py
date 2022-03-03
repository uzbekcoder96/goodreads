from django.urls import path
# from .views import BookReviewDetailAPIView,BookReviewsAPIView
from rest_framework.routers import DefaultRouter
from .views import BookReviewViewSet
app_name = 'api'

# urlpatterns = [
#     path('reviews/<int:id>/', BookReviewDetailAPIView.as_view(), name='review-detail'),
#     path('reviews/', BookReviewsAPIView.as_view(), name='review-list')
# ]

router = DefaultRouter()
router.register('reviews', BookReviewViewSet, basename='review')
urlpatterns = router.urls