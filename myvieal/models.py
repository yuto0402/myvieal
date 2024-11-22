from django.core.validators import FileExtensionValidator
from django.db import models

from accounts.models import CustomUser


class Movie(models.Model):
    title = models.CharField(max_length=128)
    explanation = models.TextField()
    movie_file = models.FileField(
        upload_to="videos/", validators=[FileExtensionValidator(allowed_extensions=["mp4", "avi", "mov", "webm"])]
    )
    number_of_views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thumbnail = models.ImageField(verbose_name='さむね', blank=True, null=True, upload_to='images/')

    def __str__(self):
        return f"{self.title} (by: {self.created_by.username})"


class Search(models.Model):
    search_word = models.CharField(max_length=128)
    searched_at = models.DateTimeField(auto_now_add=True)
    searched_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.search_word} from {self.searched_by}"
