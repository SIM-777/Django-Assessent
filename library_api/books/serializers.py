# books/serializers.py

from rest_framework import serializers
from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()  # Nested author data within the book

    class Meta:
        model = Book
        fields = '__all__'
