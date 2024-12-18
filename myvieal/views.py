# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import MovieEditForm, MovieForm, SearchHistoryForm
from .models import CustomUser, Movie, Search, MapHistory, Tag
from django.db.models import Q, Count

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_following = self.object.created_by in self.request.user.following.all()
        is_favorite = self.object in self.request.user.movie_like.all()
        like_count = self.object.like.count()

        extra_context = {
            "is_following": is_following,
            "is_favorite": is_favorite,
            "like_count": like_count,
        }
        context.update(extra_context)

        return context


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
        instance.searched_at = timezone.now()
        instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("フォームinvalid")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["histories"] = Search.objects.filter(searched_by=self.request.user)
        return context


class Following(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "myvieal/following.html"

    def get_queryset(self):
        # returnしたのを宣言するとruff-checkにやめろと言われた
        return self.request.user.following.all()

class MapHistoryView(LoginRequiredMixin, ListView):
    model = MapHistory
    template_name = 'myvieal/map_history.html'
    context_object_name = "map_histories"

    def get_queryset(self):
        return MapHistory.objects.filter(map_searched_by=self.request.user).order_by('-map_searched_at')

class MapResult(LoginRequiredMixin, ListView):
    model = Movie
    template_name = "myvieal/map.html"
    context_object_name = "movies"

    def get_queryset(self):
        order = self.request.GET.get("display_order")
        name = self.request.GET.get("name")
        address = self.request.GET.get("address")
        place_id = self.request.GET.get("placeId")
        obj = Movie.objects.filter(place_id=place_id)

        if not order and place_id:
            MapHistory.objects.create(
                map_searched_by=self.request.user,
                place_id=place_id,
                name=name,
                address=address,
                map_searched_at=timezone.now()
            )

        elif order == 'related':
            tag_count = Tag.objects.annotate(num_movies=Count('movie',filter=Q(movie__place_id=place_id)))
            movies = []
            for movie in obj:
                point = 0
                movie_tags = movie.tag_list.all()
                for tag in tag_count:
                    if tag in movie_tags:
                        point += tag.num_movies
                movies.append({'movie': movie, 'point': point})
            obj = sorted(movies, key=lambda m: m['point'], reverse=True)
            obj = [item['movie'] for item in obj]

        else:
            obj = obj.filter(place_id=place_id).order_by("-" + order)  # queryがstr型なので+演算子で文字列連結を行う

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.request.GET.get("display_order")
        place_id = self.request.GET.get('placeId')
        top_4tags = Tag.objects.filter(movie__place_id=place_id).annotate(num_movies=Count('movie', filter=Q(movie__place_id=place_id), distinct=True)).order_by('-num_movies')[:4]
        context['name'] = self.request.GET.get('name')
        context['address'] = self.request.GET.get('address')
        context['place_id'] = place_id
        context['tags'] = top_4tags
        if order == "created_at":
            context["is_searched_by_created_at"] = True
        elif order == "number_of_views":
            context["is_searched_by_numbers_of_views"] = True
        elif order == "related":
            context["is_searched_by_related"] = True
        return context

class FavoriteButtonView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_movie = Movie.objects.get(pk=request.POST.get("target_movie_pk"))
        is_favorite = target_movie in request.user.movie_like.all()
        json_context = {}
        if is_favorite:
            request.user.movie_like.remove(target_movie)
            json_context["method"] = "unfavorite"
        else:
            request.user.movie_like.add(target_movie)
            json_context["method"] = "favorite"

        json_context["like_count"] = target_movie.like.count()

        return JsonResponse(json_context)
