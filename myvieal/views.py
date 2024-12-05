# Create your views here.
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import MovieEditForm, MovieForm, SearchHistoryForm
from .models import CustomUser, Movie, Search


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
        return reverse("Profile", kwargs={"pk": self.request.user.pk})


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = "myvieal/delete.html"

    def get_success_url(self):
        return reverse("Profile", kwargs={"pk": self.request.user.pk})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.request.GET.get("display_order")
        if self.request.GET.get("search") is not None:
            context["search_text"] = self.request.GET.get("search")
        if order == "created_at":
            context["is_searched_by_created_at"] = True
        elif order == "number_of_views":
            context["is_searched_by_numbers_of_views"] = True
        print(context)
        return context

    # コンテクストデータのキーは標準では"videos_list"(モデル名_list)なので"movies"に変更
    context_object_name = "movies"


class SearchHistory(LoginRequiredMixin, CreateView):
    model = Search
    form_class = SearchHistoryForm
    template_name = "myvieal/search_history.html"

    def get_success_url(self):
        return reverse("search") + "?search=" + self.request.POST.get("search_word")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.searched_by = self.request.user
        instance.searched_at = datetime.datetime.now(tz="Asia/Tokyo")
        instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("フォームinvalid")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["histories"] = Search.objects.filter(searched_by=self.request.user)
        return context


class Following(ListView):
    model = CustomUser
    template_name = "myvieal/following.html"

    def get_queryset(self):
        # returnしたのを宣言するとruff-checkにやめろと言われた
        return self.request.user.following.all()
