from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="myvieal/entrance.html"), name="entrance"),
    path("top/", views.MovieListView.as_view(), name="top"),
    path("create/", views.MovieCreateView.as_view(), name="MovieCreate"),
    path("edit/<int:pk>/", views.MovieEditView.as_view(), name="MovieEdit"),
    path("detail/<int:pk>/", views.MovieDetailView.as_view(), name="MovieDetail"),
    path("delete/<int:pk>/", views.MovieDeleteView.as_view(), name="MovieDelete"),
    path("library/", views.LibraryView.as_view(), name="library"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("search/history", views.SearchHistory.as_view(), name="search_history"),
    path("map/history/", views.MapHistoryView.as_view(), name="MapHistory"),
    path("map/result/", views.MapResult.as_view(), name="MapResult"),
    path("favorite-button", views.FavoriteButtonView.as_view(), name="favorite_button"),
    path("tag_search/", views.SearchView.as_view(), name="tag_search"),
    path("tag/history", views.MapHistoryView.as_view(), name="tag_history"),
    path("get_tags/<str:genre_name>", views.get_tags_by_genre, name="get_tags"),
    path("create-tag/", views.CreateTagView.as_view(), name="create_tag"),
    path("privacy-policy/", TemplateView.as_view(template_name="myvieal/privacy_policy.html"), name="privacy_policy"),
    path("term-of-use/", TemplateView.as_view(template_name="myvieal/term_of_use.html"), name="term_of_use"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
