from django.contrib import admin

from .models import Comment, MapHistory, Movie, Search, Tag


class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "explanation", "movie_file", "number_of_views", "created_at", "created_by"]


class SearchAdmin(admin.ModelAdmin):
    list_display = ["search_word", "searched_at", "searched_by"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "commented_on", "commented_at", "commented_by"]


class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "genre", "number", "created_by"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(MapHistory)
