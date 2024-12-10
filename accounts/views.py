# Create your views here.
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, UpdateView
from .models import CustomUser
from .forms import BaseCustomForm, CustomSignupForm, ProfileEditForm, PasswordChangeForm

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "accounts/profile.html"

    def get_object(self, queryset=None):
        # リターンの前の宣言がいらないとruff-checkに言われた
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = self.object.movie_set.all().order_by("-created_at")
        context["movies"] = movies
        context["movie_count"] = self.object.movie_set.count()
        context["follower_count"] = self.object.followed_by.count()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "accounts/edit.html"
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse("Profile", kwargs={"pk": self.object.pk})


class UserSettingView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/setting.html"


class ProfileOthersView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "accounts/profile_others.html"

    # 共通して使う変数を設定
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = self.get_object()
        self.is_following = self.object in request.user.following.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        movies = self.object.movie_set.all().order_by("-created_at")

        extra_context = {
            "is_following": self.is_following,
            "movies": movies,
            "movie_count": movies.count(),
            "follower_count": self.object.followed_by.count(),
        }
        context.update(extra_context)
        return context

    def post(self, request, *args, **kwargs):
        json_context = {}
        if self.is_following:
            request.user.following.remove(self.object)
            json_context["method"] = "unfollow"
        else:
            request.user.following.add(self.object)
            json_context["method"] = "follow"

        json_context["follower_count"] = self.object.followed_by.count()

        return JsonResponse(json_context)


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('UserSetting')
