# books/urls.py

from django.urls import path
from .views import BookList, BookDetail, AuthorList, AuthorDetail, RegisterView, LoginView


urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<str:pk>/', BookDetail.as_view(), name='book-detail'),
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('authors/<str:pk>/', AuthorDetail.as_view(), name='author-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
