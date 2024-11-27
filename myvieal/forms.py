from django import forms

from .models import Movie


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

    title = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 1,
            }
        )
    )

    explanation = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 1,
            }
        ),
    )
