from django.contrib import admin

from .models import Movie, Search


class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "explanation", "movie_file", "number_of_views", "created_at", "created_by"]


class SearchAdmin(admin.ModelAdmin):
    list_display = ["search_word", "searched_at", "searched_by"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Search, SearchAdmin)
