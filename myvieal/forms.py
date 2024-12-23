from django import forms

from .models import Comment, Movie, Search


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
            "address",
            "name",
            "place_id",
        )


class SearchHistoryForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ("search_word",)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update(
            {
                "rows": 1,
                "cols": "",
                "placeholder": "コメントする",
                "auto_complete": "off",
            }
        )
