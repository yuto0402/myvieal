from django.contrib import admin

from .models import Follow, Movie, Search


class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "explanation", "movie_file", "number_of_views", "created_at", "created_by"]


class FollowAdmin(admin.ModelAdmin):
    list_display = ["from_user", "to_user"]


class SearchAdmin(admin.ModelAdmin):
    list_display = ["search_word", "searched_at", "searched_by"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Search, SearchAdmin)
