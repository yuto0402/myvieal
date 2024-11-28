from django.urls import path

from . import views

urlpatterns = [
    path("top/", views.MovieListView.as_view(), name="top"),
    path("create/", views.MovieCreateView.as_view(), name="MovieCreate"),
    path("edit/<int:pk>/", views.MovieEditView.as_view(), name="MovieEdit"),
    path("detail/<int:pk>/", views.MovieDetailView.as_view(), name="MovieDetail"),
    path("delete/<int:pk>/", views.MovieDeleteView.as_view(), name="MovieDelete"),
    path("following/", views.Following.as_view(), name="following"),
]
