from django import forms

from .models import Movie, Search


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = (
            "title",
            "explanation",
            "movie_file",
            "thumbnail",
        )


class MovieEditForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = (
            "title",
            "explanation",
            "thumbnail",
        )


class SearchHistoryForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ("search_word",)
