from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class AbstractCategoryGenreModel(models.Model):
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        abstract = True
        ordering = ('-id', 'name',)

    def __str__(self):
        return self.name


class AbstractReviewCommentModel(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-id', '-pub_date', )

    def __str__(self):
        return self.text[:settings.TEXT_CUTTER_30]


class Category(AbstractCategoryGenreModel):
    slug = models.SlugField(
        max_length=settings.SLUG_LENGTH, unique=True,
        verbose_name='Slug категории', db_index=True
    )

    class Meta(AbstractCategoryGenreModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractCategoryGenreModel):
    slug = models.SlugField(
        max_length=settings.SLUG_LENGTH, unique=True,
        verbose_name='Slug жанра', db_index=True
    )

    class Meta(AbstractCategoryGenreModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=settings.TITLE_NAME_LENGTH,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(datetime.now().year),
            MinValueValidator(1)
        ],
        null=True,
        verbose_name='Год создания произведения'
    )
    description = models.TextField(verbose_name='Описание произведения')
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        db_index=True,
        blank=True,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-name',)

    def __str__(self):
        return self.name[:settings.TEXT_CUTTER_50]


class Review(AbstractReviewCommentModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    score = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Оценка должна быть больше или равна 1.'
            ),
            MaxValueValidator(
                limit_value=10,
                message='Оценка должна быть меньше или равна 10.'
            )
        ]
    )

    class Meta(AbstractReviewCommentModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_per_author'
            )
        ]


class Comment(AbstractReviewCommentModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментарий'
    )

    class Meta(AbstractReviewCommentModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
