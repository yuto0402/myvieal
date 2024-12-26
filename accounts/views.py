# Create your views here.
from typing import Any

from allauth.account.views import SignupView
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import DeleteView, DetailView, TemplateView, UpdateView

from .adapter import CustomAccountAdapter
from .forms import (
    CustomPasswordResetForm,
    CustomUserCreationForm,
    EmailChangeCodeForm,
    EmailChangeForm,
    EmailConfirmationForm,
    EmailVerificationCodeForm,
    PasswordChangeForm,
    ProfileEditForm,
    VerificationCodeForm,
)
from .models import CustomUser


def redirect_if_authenticated(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("top")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


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


@redirect_if_authenticated
def signup_email_view(request):
    if request.session.get("signup_email"):
        return redirect(reverse("account_signup_email_confirmation"))
    if request.method == "POST":
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            false_user = get_user_model().objects.filter(email=email, is_active=False)
            if false_user.exists():
                false_user = false_user.first()
                uid = urlsafe_base64_encode(force_bytes(false_user.pk))
                token = default_token_generator.make_token(false_user)
                if request.session.get("email_verification_code"):
                    del request.session["email_verification_code"]
                return redirect(reverse("account_signup_true", kwargs={"uidb64": uid, "token": token}))
            form.save(request)
            return redirect(reverse("account_signup_email_confirmation"))
    else:
        form = EmailConfirmationForm()

    return render(request, "account/signup_email.html", {"form": form})


@redirect_if_authenticated
def signup_email_confirmation_view(request):
    email = request.session.get("signup_email")
    if not email:
        return redirect(reverse("account_signup"))
    max_attempts = 3

    if request.method == "POST":
        form = EmailVerificationCodeForm(request.POST, request=request)
        if form.is_valid():
            username = CustomAccountAdapter.generate_unique_username()
            false_user = get_user_model().objects.create_user(email=email, username=username, is_active=False)
            uid = urlsafe_base64_encode(force_bytes(false_user.pk))
            token = default_token_generator.make_token(false_user)
            request.session["signup_email_true"] = email
            if request.session.get("email_verification_code"):
                del request.session["email_verification_code"]
            del request.session["signup_email"]
            if request.session.get("attempts"):
                del request.session["attempts"]
            return redirect(reverse("account_signup_true", kwargs={"uidb64": uid, "token": token}))
        attempts = request.session.get("attempts", 0)
        attempts += 1
        request.session["attempts"] = attempts
        if attempts >= max_attempts:
            if request.session.get("email_verification_code"):
                del request.session["email_verification_code"]
            if request.session.get("signup_email"):
                del request.session["signup_email"]
            if request.session.get("attempts"):
                del request.session["attempts"]
            return redirect(reverse("account_signup_email_confirmation"))
    else:
        form = EmailVerificationCodeForm()

    return render(request, "account/signup_email_confirmation.html", {"form": form, "email": email})


@redirect_if_authenticated
def signup_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            return redirect(reverse("account_signup"))

    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        return redirect(reverse("account_signup"))

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if not request.session.get("signup_email_true"):
                return redirect(reverse("account_signup"))
            user.username = form.cleaned_data["username"]
            user.set_password(form.cleaned_data["password1"])
            user.is_active = True
            user.save()
            del request.session["signup_email_true"]
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            return redirect(reverse("top"))

    else:
        form = CustomUserCreationForm(
            initial={
                "email": user.email,
            }
        )

    return render(request, "account/signup.html", {"form": form})


@redirect_if_authenticated
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
    email = request.session.get("signup_email")
    if not email:
        return JsonResponse({"error": "セッションにメールアドレスがありません。"}, status=400)
    email_verification_code = CustomAccountAdapter()._generate_code()
    if request.session.get("attempts"):
        del request.session["attempts"]
    request.session["email_verification_code"] = email_verification_code
    request.session["signup_email"] = email
    EmailConfirmationForm().send_verification_code(email, email_verification_code)
    form = EmailVerificationCodeForm()
    post_success = True

    return render(
        request, "account/signup_email_confirmation.html", {"form": form, "post_success": post_success, "email": email}
    )


def resend_password_reset(request):
    post_success = False
    if request.method != "POST":
        return JsonResponse({"error": "無効なリクエストメソッドです。"}, status=405)
    email = request.session.get("password_reset_email")
    if not email:
        return JsonResponse({"error": "セッションにメールアドレスがありません。"}, status=400)
    for user in CustomPasswordResetForm().get_users(email):
        verification_code = CustomAccountAdapter()._generate_code()
        CustomPasswordResetForm().send_verification_code(user.email, verification_code)
        request.session["verification_code"] = verification_code
    form = CustomPasswordResetForm
    post_success = True

    return render(
        request, "account/password_reset_done.html", {"form": form, "post_success": post_success, "email": email}
    )


def resend_email_change(request):
    post_success = False
    if request.method != "POST":
        return JsonResponse({"error": "無効なリクエストメソッドです。"}, status=405)
    email = request.session.get("new_email")
    if not email:
        return JsonResponse({"error": "セッションにメールアドレスがありません。"}, status=400)
    email_change_code = CustomAccountAdapter()._generate_code()
    if request.session.get("attempts"):
        del request.session["attempts"]
    request.session["email_change_code"] = email_change_code
    request.session["new_email"] = email
    EmailChangeForm().send_verification_code(email, email_change_code)
    form = EmailChangeCodeForm()
    post_success = True

    return render(
        request, "accounts/email_change_confirmation.html", {"form": form, "post_success": post_success, "email": email}
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


@login_required
def email_change_view(request):
    email = request.user.email
    if request.session.get("new_email"):
        return redirect(reverse("EmailChangeConfirmation"))
    if request.method == "POST":
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect(reverse("EmailChange"))
    else:
        form = EmailChangeForm()

    return render(request, "accounts/email_change.html", {"form": form, "email": email})


@login_required
def email_change_confirmation_view(request):
    email = request.session.get("new_email")
    if not email:
        return redirect(reverse("EmailChange"))
    max_attempts = 3

    if request.method == "POST":
        form = EmailChangeCodeForm(request.POST, request=request)
        if form.is_valid():
            request.user.email = email
            request.user.save()
            del request.session["email_change_code"]
            del request.session["new_email"]
            if request.session.get("attempts"):
                del request.session["attempts"]
            return redirect(reverse("UserSetting"))
        attempts = request.session.get("attempts", 0)
        attempts += 1
        request.session["attempts"] = attempts
        if attempts >= max_attempts:
            if request.session.get("email_change_code"):
                del request.session["email_change_code"]
            if request.session.get("new_email"):
                del request.session["new_email"]
            if request.session.get("attempts"):
                del request.session["attempts"]
            return redirect(reverse("UserSetting"))
    else:
        form = EmailChangeCodeForm()

    return render(request, "accounts/email_change_confirmation.html", {"form": form, "email": email})


def session_initializer(request):
    if request.method != "POST":
        return JsonResponse({"error": "無効なリクエストメソッドです。"}, status=405)
    if request.session.get("email_change_code"):
        del request.session["email_change_code"]
    if request.session.get("new_email"):
        del request.session["new_email"]
    if request.session.get("attempts"):
        del request.session["attempts"]
    return render(request, "accounts/setting.html")


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("UserSetting")


class AccountDeleteView(DeleteView):
    model = CustomUser
    template_name = "accounts/account_delete.html"
    success_url = reverse_lazy("deleted")


class FollowButtonView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_user = CustomUser.objects.get(pk=request.POST.get("target_user_pk"))
        is_following = target_user in request.user.following.all()
        json_context = {}
        if is_following:
            request.user.following.remove(target_user)
            json_context["method"] = "unfollow"
        else:
            request.user.following.add(target_user)
            json_context["method"] = "follow"

        json_context["follower_count"] = target_user.followed_by.count()

        return JsonResponse(json_context)
