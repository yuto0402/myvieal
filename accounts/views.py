# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, UpdateView

from .forms import ProfileEditForm
from .models import CustomUser


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "accounts/profile.html"

    def get_object(self, queryset=None):
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
