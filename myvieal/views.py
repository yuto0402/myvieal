# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Movie
from accounts.models import CustomUser
from .forms import MovieForm, MovieEditForm

# Create your views here.
class MovieListView(LoginRequiredMixin, ListView):
    template_name = 'myvieal/top.html'
    model = Movie
    context_object_name = 'movies'
    ordering = ['-created_at']

class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    template_name = 'myvieal/create.html'
    form_class = MovieForm
    success_url = reverse_lazy('top')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.created_by = self.request.user
        object.save()
        return  super().form_valid(form)

class MovieDetailView(LoginRequiredMixin, DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'myvieal/detail.html'

    def get_object(self, queryset=None):
        movie = super().get_object(queryset)
        movie.number_of_views += 1
        movie.save()
        return movie

class MovieEditView(LoginRequiredMixin, UpdateView):
    model = Movie
    template_name = 'myvieal/edit.html'
    form_class = MovieEditForm

    def get_success_url(self):
        return reverse('MovieDetail', kwargs={'pk': self.object.pk})

class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = 'myvieal/delete.html'
    success_url = reverse_lazy('top')

class Following(ListView):
    model = CustomUser
    template_name = "myvieal/following.html"

    def get_queryset(self):
        # returnしたのを宣言するとruff-checkにやめろと言われた
        return self.request.user.following.all()