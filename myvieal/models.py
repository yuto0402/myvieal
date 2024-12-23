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
    thumbnail = models.ImageField(verbose_name="さむね", blank=True, null=True, upload_to="images/")
    like = models.ManyToManyField(CustomUser, related_name="movie_like")
    tag_list = models.ManyToManyField("Tag", related_name="movie")
    address = models.CharField(verbose_name="住所", max_length=255, null=True)
    name = models.CharField(verbose_name="施設名", max_length=255, default="Untitled")
    place_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.title} (by: {self.created_by.username})"


class Search(models.Model):
    search_word = models.CharField(max_length=128)
    searched_at = models.DateTimeField(auto_now_add=True)
    searched_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.search_word} from {self.searched_by}"


class Comment(models.Model):
    content = models.TextField()
    commented_on = models.ForeignKey(Movie, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content} (by: {self.commented_by} on: {self.commented_on})"


class Tag(models.Model):
    GENRE_LIST = [
        ("animals", "動物"),
        ("food", "食べ物"),
        ("locations", "場所"),
        ("anime", "アニメ"),
        ("movies", "映画"),
        ("gaming", "ゲーム"),
        ("electronic_equipment", "電子機器"),
        ("sports", "スポーツ"),
        ("music", "音楽"),
        ("art", "アート"),
        ("culture", "文化"),
        ("science", "科学"),
        ("history", "歴史"),
        ("literature", "文学"),
        ("fashion", "ファッション"),
        ("person", "人物"),
        ("health", "健康"),
        ("education", "教育"),
        ("business", "ビジネス"),
        ("politics", "政治"),
        ("social_issues", "社会問題"),
        ("nature", "自然"),
        ("events", "イベント"),
        ("feeling", "感覚"),
        ("misc", "その他"),
    ]

    name = models.CharField(max_length=128)
    genre = models.CharField(max_length=128, choices=GENRE_LIST)
    number = models.IntegerField(default=0)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}({self.genre})"


class MapHistory(models.Model):
    address = models.CharField(verbose_name="住所", max_length=255, null=True)
    name = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255, null=True)
    map_searched_at = models.DateTimeField(auto_now_add=True)
    map_searched_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
