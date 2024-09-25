# books/models.py

from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, blank=True)
    average_rating = models.FloatField()
    ratings_count = models.IntegerField()
    text_reviews_count = models.IntegerField()
    fans_count = models.IntegerField()
    image_url = models.URLField(blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    language = models.CharField(max_length=20)
    average_rating = models.FloatField()
    rating_dist = models.CharField(max_length=255)
    ratings_count = models.IntegerField()
    text_reviews_count = models.IntegerField()
    publication_date = models.CharField(max_length=20, blank=True)
    original_publication_date = models.CharField(max_length=20, blank=True)
    format = models.CharField(max_length=100, blank=True)
    edition_information = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    num_pages = models.IntegerField()
    series_id = models.CharField(max_length=255, blank=True)
    series_name = models.CharField(max_length=255, blank=True)
    series_position = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)