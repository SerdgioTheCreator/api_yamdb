from django.contrib import admin
from .models import Categories, Genre, Title


admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Categories)
