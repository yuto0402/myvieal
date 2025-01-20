from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import ProfileEditForm
from django.contrib.auth import login

# Create your tests here.
class ProfileViewTest(TestCase):
  def setUp(self):
    self.user = CustomUser.objects.create_user(username="testuser", password="password", email="test@example.com")
    self.client.login(username="testuser", password="password")
    self.profile_user = CustomUser.objects.create_user(username="profileuser", password="password", email="profile@example.com")

  def test_profile(self):
    response = self.client.get(reverse("Profile", kwargs={"pk": self.profile_user.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "accounts/profile.html")
    self.assertEqual(response.context["user"], self.profile_user)
    self.assertEqual(response.context["movie_count"], 0)

  def test_profile_user_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("Profile", kwargs={"pk": self.user.pk}))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse("Profile", kwargs={"pk": self.user.pk})}", status_code=302, target_status_code=200)

class ProfileEditViewTest(TestCase):
  def setUp(self):
    self.user = CustomUser.objects.create_user(username="testuser", password="password", email="test@example.com")
    self.client.login(username="testuser", password="password")

  def test_profile_edit(self):
    response = self.client.get(reverse("ProfileEdit", kwargs={"pk": self.user.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'accounts/edit.html')
    self.assertIsInstance(response.context["form"], ProfileEditForm)
    form = response.context["form"]
    self.assertEqual(form.initial["username"], self.user.username)

  def test_profile_edit_submit(self):
    response = self.client.get(reverse("ProfileEdit", kwargs={"pk": self.user.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "accounts/edit.html")
    self.assertIsInstance(response.context["form"], ProfileEditForm)
    response = self.client.post(
      reverse("ProfileEdit", kwargs={"pk": self.user.pk}),
      {
        "username": "newusername",
        "introduction": "New Introduction",
        "icon_image": "New IconImage",
      },
    )
    self.assertRedirects(response, reverse("Profile", kwargs={"pk": self.user.pk}))
    self.user.refresh_from_db()
    self.assertEqual(self.user.username, "newusername")
    self.assertEqual(self.user.introduction, "New Introduction")

  def test_profile_edit_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("ProfileEdit", kwargs={"pk": self.user.pk}))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse("ProfileEdit", kwargs={"pk": self.user.pk})}", status_code=302, target_status_code=200)

class UserSettingViewTest(TestCase):
  def setUp(self):
    self.user = CustomUser.objects.create_user(username="testuser", password="password", email="test@example.com")
    self.client.login(username="testuser", password="password")

  def test_user_setting(self):
    response = self.client.get(reverse("UserSetting"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "accounts/setting.html")

  def test_user_setting_user_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("UserSetting"))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('UserSetting')}", status_code=302, target_status_code=200)
