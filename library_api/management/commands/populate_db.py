import random
from faker import Faker
from django.core.management.base import BaseCommand
from library_api.models import Author, Book

fake = Faker()

class Command(BaseCommand):
    help = "Populates the database with dummy authors and books"

    def handle(self, *args, **kwargs):
        self.create_authors_and_books()

    def create_authors_and_books(self):
        # Create 10 dummy authors
        for _ in range(10):
            author = Author.objects.create(
                id=fake.uuid4(),
                name=fake.name(),
                gender=random.choice(['Male', 'Female', '']),
                average_rating=round(random.uniform(3.0, 5.0), 2),
                ratings_count=random.randint(1000, 100000),
                text_reviews_count=random.randint(0, 1000),
                fans_count=random.randint(0, 5000),
                image_url=fake.image_url(),
                about=fake.text()
            )
            self.stdout.write(self.style.SUCCESS(f"Created author: {author.name}"))

            # For each author, create 5-10 books
            for _ in range(random.randint(5, 10)):
                book = Book.objects.create(
                    id=fake.uuid4(),
                    title=fake.sentence(nb_words=5),
                    author=author,
                    isbn=fake.isbn10(),
                    isbn13=fake.isbn13(),
                    language=random.choice(['eng', 'fre', 'spa', 'ger', 'ita']),
                    average_rating=round(random.uniform(3.0, 5.0), 2),
                    rating_dist=f"5:{random.randint(100, 500)}|4:{random.randint(100, 500)}|3:{random.randint(100, 500)}|2:{random.randint(100, 500)}|1:{random.randint(100, 500)}|total:{random.randint(500, 2000)}",
                    ratings_count=random.randint(500, 2000),
                    text_reviews_count=random.randint(10, 200),
                    publication_date=fake.date_this_century().strftime("%Y-%m"),
                    original_publication_date=fake.date_this_century().strftime("%Y-%m-%d"),
                    format=random.choice(['Paperback', 'Hardcover', 'Ebook']),
                    edition_information=fake.catch_phrase(),
                    image_url=fake.image_url(),
                    publisher=fake.company(),
                    num_pages=random.randint(100, 1000),
                    series_id=fake.uuid4() if random.choice([True, False]) else '',
                    series_name=fake.sentence(nb_words=3) if random.choice([True, False]) else '',
                    series_position=str(random.randint(1, 10)) if random.choice([True, False]) else '',
                    description=fake.text()
                )
                self.stdout.write(self.style.SUCCESS(f"Created book: {book.title} by {author.name}"))

        self.stdout.write(self.style.SUCCESS('Database populated with dummy data!'))