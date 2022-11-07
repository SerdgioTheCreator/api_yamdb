from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


class AbstractModel(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        abstract = True
        ordering = ['-id', 'name']

    def __str__(self):
        return self.name


class Categories(AbstractModel):
    slug = models.SlugField(
        max_length=50, unique=True, null=True,
        verbose_name='Slug категории', db_index=True
    )

    class Meta(AbstractModel.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(AbstractModel):
    slug = models.SlugField(
        max_length=50, unique=True, null=True,
        verbose_name='Slug жанра', db_index=True
    )

    class Meta(AbstractModel.Meta):
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.CharField(max_length=300)
    year = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(datetime.now().year),
            MinValueValidator(1)
        ],
        null=True,
        verbose_name='Год создания произведения'
    )
    # rating =
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        db_index=True,
        blank=True,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-name']

    def __str__(self):
        return self.name[:50]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Score should be equal or higher than 1.'
            ),
            MaxValueValidator(
                limit_value=10,
                message='Score should be equal or less than 10.'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_per_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['-id']

    def __str__(self):
        return self.text
