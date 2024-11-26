# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.models import CustomUser

from .forms import MovieEditForm, MovieForm
from .models import Movie


# Create your views here.
class MovieListView(LoginRequiredMixin, ListView):
    template_name = "myvieal/top.html"
    model = Movie
    context_object_name = "movies"
    ordering = ["-created_at"]


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    template_name = "myvieal/create.html"
    form_class = MovieForm
    success_url = reverse_lazy("top")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        return super().form_valid(form)


class MovieDetailView(LoginRequiredMixin, DetailView):
    model = Movie
    context_object_name = "movie"
    template_name = "myvieal/detail.html"

    def get_object(self, queryset=None):
        movie = super().get_object(queryset)
        movie.number_of_views += 1
        movie.save()
        return movie


class MovieEditView(LoginRequiredMixin, UpdateView):
    model = Movie
    template_name = "myvieal/edit.html"
    form_class = MovieEditForm

    def get_success_url(self):
        return reverse("MovieDetail", kwargs={"pk": self.object.pk})


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = "myvieal/delete.html"
    success_url = reverse_lazy("top")


class SearchView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = "myvieal/search.html"

    def get_queryset(self):
        obj = Movie.objects.all()
        order = self.request.GET.get("display_order")
        search = self.request.GET.get("search")
        if order is not None:
            obj = obj.order_by("-" + order)  # queryがstr型なので+演算子で文字列連結を行う
        if search is not None:
            obj = obj.filter(title__icontains=search)
        return obj

    # コンテクストデータのキーは標準では"videos_list"(モデル名_list)なので"objects"に変更
    context_object_name = "movies"


class Following(ListView):
    model = CustomUser
    template_name = "myvieal/following.html"

    def get_queryset(self):
        # returnしたのを宣言するとruff-checkにやめろと言われた
        return self.request.user.following.all()
