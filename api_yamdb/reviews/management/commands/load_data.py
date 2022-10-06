from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User

FILE_PATH = {
    'users': 'static/data/users.csv',
    'category': 'static/data/category.csv',
    'genre': 'static/data/genre.csv',
    'title': 'static/data/titles.csv',
    'genre_title': 'static/data/genre_title.csv',
    'review': 'static/data/review.csv',
    'comments': 'static/data/comments.csv',
}


class Command(BaseCommand):
    help = """
        Loads data from csv 'file'.
        If something goes wrong when you load data from the CSV file,
        first delete the db.sqlite3 file to destroy the database.
        Then, run `python manage.py migrate` for a new empty
        database with tables.
        """

    COUNT = {
        'user': {'created': 0, 'got': 0},
        'category': {'created': 0, 'got': 0},
        'genre': {'created': 0, 'got': 0},
        'title': {'created': 0, 'got': 0},
        'review': {'created': 0, 'got': 0},
        'comments': {'created': 0, 'got': 0},
    }

    def load_user_data(self):
        with open(FILE_PATH['users'], 'r', encoding='utf-8') as csv_file:
            file_reader = DictReader(csv_file)
            for row in file_reader:
                obj, created = User.objects.get_or_create(**row)
                if created:
                    self.COUNT['user']['created'] += 1
                else:
                    self.COUNT['user']['got'] += 1

    def load_category_data(self):
        with open(FILE_PATH['category'], 'r', encoding='utf-8') as csv_file:
            file_reader = DictReader(csv_file)
            for row in file_reader:
                obj, created = Category.objects.get_or_create(**row)
                if created:
                    self.COUNT['category']['created'] += 1
                else:
                    self.COUNT['category']['got'] += 1

    def load_genre_data(self):
        with open(FILE_PATH['genre'], 'r', encoding='utf-8') as csv_file:
            file_reader = DictReader(csv_file)
            for row in file_reader:
                obj, created = Genre.objects.get_or_create(**row)
                if created:
                    self.COUNT['genre']['created'] += 1
                else:
                    self.COUNT['genre']['got'] += 1

    def load_title_data(self):
        with open(FILE_PATH['title'], 'r', encoding='utf-8') as csv_file:
            file_reader = DictReader(csv_file)
            for row in file_reader:
                obj, created = Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(pk=row['category']),
                )
                if created:
                    self.COUNT['title']['created'] += 1
                else:
                    self.COUNT['title']['got'] += 1

    def load_genre_title_data(self):
        with open(FILE_PATH['genre_title'], 'r', encoding='utf-8') as csv_file:
            file_reader = DictReader(csv_file)
            for row in file_reader:
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                title.genre.add(genre)

    def load_review_data(self):
        with open(FILE_PATH['review'], 'r', encoding='utf-8') as csv_file:
            file_reader = DictReader(csv_file)
            for row in file_reader:
                obj, created = Review.objects.get_or_create(
                    id=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                if created:
                    self.COUNT['review']['created'] += 1
                else:
                    self.COUNT['review']['got'] += 1

    def load_comment_data(self):
        with open(FILE_PATH['comments'], 'r', encoding='utf-8') as csv_file:
            file_reader = DictReader(csv_file)
            for row in file_reader:
                obj, created = Comments.objects.get_or_create(
                    id=row['id'],
                    review=Review.objects.get(pk=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    pub_date=row['pub_date'],
                )
                if created:
                    self.COUNT['comments']['created'] += 1
                else:
                    self.COUNT['comments']['got'] += 1

    def handle(self, *args, **options):
        self.load_user_data()
        self.load_category_data()
        self.load_genre_data()
        self.load_title_data()
        self.load_genre_title_data()
        self.load_review_data()
        self.load_comment_data()

        for key, value in self.COUNT.items():
            self.stdout.write(f' model {key.title()}:'
                              f' objects created {value["created"]},'
                              f' objects got {value["got"]}')
        self.stdout.write(self.style.SUCCESS('Successful data load'))
