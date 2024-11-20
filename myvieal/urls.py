from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('top/', views.MovieListView.as_view(), name='top'),
    path('create/', views.MovieCreateView.as_view(), name='MovieCreate'),
    path('edit/', views.MovieEditView.as_view(), name='MovieEdit'),
    path('detail/<int:pk>/', views.MovieDetailView.as_view(), name='MovieDetail'),
]
