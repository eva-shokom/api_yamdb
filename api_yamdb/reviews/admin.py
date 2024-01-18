from django.contrib import admin

from .models import Categories, Genres, Title, Review, Comment


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):

    list_display = ('name', 'year', 'category')
    list_filter = ('category', 'genre')
    search_fields = ('name', 'year', 'category__name')
    filter_horizontal = ('genre',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('review', 'author', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('review__title__name', 'author__username')
    ordering = ('-pub_date',)


@admin.register(Genres)
class GenreAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('title__name', 'author__username')
    ordering = ('-pub_date',)
