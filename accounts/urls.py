from allauth.account.urls import urlpatterns as account_urlpatterns
from django.contrib.auth.views import LogoutView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetView
from django.urls import include, path

from . import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from .views import CustomSignupView

filtered_account_urlpatterns = [
    url
    for url in account_urlpatterns
    if url.name
    not in [
        "account_logout",
        "account_signup",
        "account_reset_password",
        "account_reset_password_done",
        "account_reset_password_from_key",
        "account_reset_password_from_key_done",
    ]
]

urlpatterns = [
    path("", include(filtered_account_urlpatterns)),
    path("logout/", LogoutView.as_view(next_page="entrance"), name="account_logout"),
    path("signup/", CustomSignupView.as_view(), name="account_signup"),
    path(
        "password/reset/",
        PasswordResetView.as_view(template_name="account/password_reset.html", form_class=CustomPasswordResetForm),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        views.code_verification_view,
        name="password_reset_done",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="account/password_reset_from_key.html", form_class=CustomSetPasswordForm
        ),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        PasswordResetCompleteView.as_view(template_name="account/password_reset_from_key_done.html"),
        name="password_reset_complete",
    ),
    path("resend/", views.resend_otp, name="resend"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="Profile"),
    path("edit/<int:pk>/", views.ProfileEditView.as_view(), name="ProfileEdit"),
    path("setting/", views.UserSettingView.as_view(), name="UserSetting"),
    path("profile-others/<int:pk>", views.ProfileOthersView.as_view(), name="ProfileOthers"),
    path("password_change", views.PasswordChangeView.as_view(), name="PasswordChange"),
]
