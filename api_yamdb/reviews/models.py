from django.db import models
from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(
        max_length=50, unique=True, null=True,
        verbose_name='Slug категории', db_index=True
    )


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(
        unique=True, max_length=50, null=True,
        verbose_name='Slug жанра', db_index=True
    )


class Title(models.Model):
    name = models.CharField(max_length=300)
    year = models.IntegerField()
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
    score = models.IntegerField(blank=True, null=True)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

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

    def __str__(self):
        return self.text
