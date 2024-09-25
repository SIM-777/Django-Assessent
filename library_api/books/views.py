# books/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Book, Favorite
from .serializers import BookSerializer
# Book Views
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(author__name__icontains=search_query)
            )
        return queryset

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Author Views
class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
        

class FavoriteBookList(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)
        # Add book to favorites
        if Favorite.objects.filter(user=request.user).count() >= 20:
            return Response({'error': 'You can only have a maximum of 20 favorite books.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
         Favorite.objects.create(user=request.user, book=book)
         recommendations = self.get_recommendations(book.author_name)

            # Return the list of recommended books
        return Response({
                'message': 'Book added to favorites.',
                'recommendations': recommendations
            }, status=status.HTTP_201_CREATED)

    def get_recommendations(self, author_name):
        # Find books by the same author, excluding those already in the user's favorites
        favorite_books = Favorite.objects.filter(user=self.request.user).values_list('book__id', flat=True)
        recommended_books = Book.objects.filter(author_name=author_name).exclude(id__in=favorite_books)[:5]
        
        # Serialize the recommended books and return them
        return BookSerializer(recommended_books, many=True).data        