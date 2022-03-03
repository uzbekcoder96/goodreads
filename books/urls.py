from django.urls import path
from .views import  BooksView, BookDetailView, AddReviewView, EditReviewView, DeleteReviewConfirmView, DeleteReviewView

app_name = 'books'
urlpatterns = [
    
    path('books/', BooksView.as_view(), name="list"),
    path('books/<int:id>', BookDetailView.as_view(), name="detail"),
    path('<int:id>/reviews', AddReviewView.as_view(), name='review'),
    path('<int:book_id>/reviews/<int:review_id>/edit', EditReviewView.as_view(), name='edit-review'),
    path('<int:book_id>/reviews/<int:review_id>/delete/confirm', DeleteReviewConfirmView.as_view(), name='delete-review-confirm'),
    path('<int:book_id>/reviews/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete-review')
]