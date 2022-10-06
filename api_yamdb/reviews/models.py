from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import check_year

MAX_REVIEW_SCORE = 10
MIN_REVIEW_SCORE = 1


class Category(models.Model):
    """
    Категории произведений
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=64,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Жанры произведений.
    Одно произведение может быть привязано к нескольким жанрам.
    """
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=128,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=64,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы.
    """
    name = models.TextField(
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=(check_year,)
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='genre_title'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        ordering = ['name']

    def __str__(self):
        return self.name


class BaseReview(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s'
    )
    pub_date = models.DateTimeField(
        default=datetime.now,
        editable=False,
        verbose_name='Дата публикации',
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Review(BaseReview):
    """
    Отзывы на произведения.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(MAX_REVIEW_SCORE),
            MinValueValidator(MIN_REVIEW_SCORE)
        ]
    )

    class Meta(BaseReview.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(BaseReview):
    """
    Комментарии к отзывам.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta(BaseReview.Meta):
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
