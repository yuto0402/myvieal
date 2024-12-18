from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="myvieal/entrance.html"), name="entrance"),
    path("top/", views.MovieListView.as_view(), name="top"),
    path("create/", views.MovieCreateView.as_view(), name="MovieCreate"),
    path("edit/<int:pk>/", views.MovieEditView.as_view(), name="MovieEdit"),
    path("detail/<int:pk>/", views.MovieDetailView.as_view(), name="MovieDetail"),
    path("delete/<int:pk>/", views.MovieDeleteView.as_view(), name="MovieDelete"),
    path("following/", views.Following.as_view(), name="following"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("search/history", views.SearchHistory.as_view(), name="search_history"),
    path("map/history/", views.MapHistoryView.as_view(), name="MapHistory"),
    path("map/result/", views.MapResult.as_view(), name="MapResult"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
