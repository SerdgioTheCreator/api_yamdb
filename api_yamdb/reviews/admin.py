from django.contrib import admin
from .models import Categories, Genre, Title, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year',
                    'category')
    empty_value_display = '-пусто-'


admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Categories)
admin.site.register(Review)
admin.site.register(Comment)
