from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q

from .validators import validate_year


User = get_user_model()


class Categories(models.Model):
    """Категории."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Имя категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории',
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Genres(models.Model):
    """Жанры."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год',
        validators=(validate_year,)
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genres,
        through='TitleGenres',
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class TitleGenres(models.Model):
    """Жанры и произведеня(Many to many)."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',)
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение-Жанр'
        verbose_name_plural = 'Произведения-Жанры'
        ordering = ('genre',)

    def __str__(self):
        return f'{self.title}-{self.genre}'


class Review(models.Model):
    """Отзывы."""

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0, message='Нельзя поставить оценку ниже 0'),
            MaxValueValidator(10, message='Нельзя поставить оценку выше 10')
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-score',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
            models.CheckConstraint(
                check=~Q(author=F('title')),
                name='could_have_only_one_review'
            )
        ]

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    """Комментарии."""

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:20]
