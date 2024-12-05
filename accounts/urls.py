from django.urls import include, path

from . import views

urlpatterns = [
    path("", include("allauth.urls")),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="Profile"),
    path("edit/<int:pk>/", views.ProfileEditView.as_view(), name="ProfileEdit"),
    path("setting/", views.UserSettingView.as_view(), name="UserSetting"),
    path('password_change', views.PasswordChangeView.as_view(), name='PasswordChange'),
]
