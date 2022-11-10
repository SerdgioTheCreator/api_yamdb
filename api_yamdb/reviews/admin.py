from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from .models import Category, Genre, Title, Review, Comment
from reviews.forms import TitleListForm


class TitleChangeList(ChangeList):

    def __init__(self, request, model, list_display, list_display_links,
                 list_filter, date_hierarchy, search_fields, list_select_related,
                 list_per_page, list_max_show_all, list_editable, model_admin, sortable_by,):
        super(TitleChangeList, self).__init__(request, model,
                                              list_display, list_display_links, list_filter,
                                              date_hierarchy, search_fields, list_select_related,
                                              list_per_page, list_max_show_all, list_editable,
                                              model_admin, sortable_by,)

        # these need to be defined here, and not in ItemAdmin
        self.list_display = ['pk', 'name', 'year',
                             'category', 'gig_genre']
        self.list_display_links = ['name']
        self.list_editable = ['genre']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):

    def get_changelist(self, request, **kwargs):
        return TitleChangeList

    def get_changelist_form(self, request, **kwargs):
        return TitleListForm


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)
admin.site.register(Comment)
