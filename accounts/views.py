# Create your views here.


from typing import Any

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from allauth.account.views import SignupView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import DetailView, TemplateView, UpdateView

from .forms import PasswordChangeForm, ProfileEditForm, VerificationCodeForm
from .models import CustomUser


class CustomSignupView(SignupView):
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if email:
            self.request.session["email_for_verification"] = email
        return super().form_valid(form)


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


def code_verification_view(request):
    email = request.session.get("password_reset_email")

    if request.method == "POST":
        form = VerificationCodeForm(request.POST, request=request)
        if form.is_valid():
            email = request.session.get("password_reset_email")
            user = get_user_model().objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            del request.session["verification_code"]
            del request.session["password_reset_email"]
            return redirect(reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token}))
    else:
        form = VerificationCodeForm()

    return render(request, "account/password_reset_done.html", {"form": form, "email": email})


def resend_otp(request):
    post_success = False
    if request.method != "POST":
        return JsonResponse({"error": "無効なリクエストメソッドです。"}, status=405)
    email = request.session.get("email_for_verification")
    if not email:
        return JsonResponse({"error": "セッションにメールアドレスがありません。"}, status=400)
    email_address = EmailAddress.objects.filter(email=email, verified=False).first()
    if not email_address:
        return JsonResponse({"error": "未確認のメールアドレスが見つかりません。"}, status=400)
    send_email_confirmation(request, email_address.user, signup=False)
    post_success = True

    return render(
        request, "account/confirm_email_verification_code.html", {"post_success": post_success, "email": email}
    )


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
    template_name = "accounts/password_change.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("UserSetting")
