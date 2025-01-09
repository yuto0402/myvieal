from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class FollowButtonTest(TestCase):
    def setUp(self):
        self.tester_user = CustomUser.objects.create_user("tester")
        self.test_user_followed = CustomUser.objects.create_user("test_followed")

    def test_request_by_get(self):
        self.client.force_login(self.tester_user)
        response = self.client.get(reverse("follow_button"))
        self.assertEqual(response.status_code, 405)

    def test_user_is_not_logined(self):
        response = self.client.post(reverse("follow_button"))
        self.assertRedirects(
            response,
            f"{reverse("account_login")}?next={reverse("follow_button")}",
            status_code=302,
            target_status_code=200,
        )

    def test_user_is_not_following_target_user(self):
        self.client.force_login(self.tester_user)
        response = self.client.post(reverse("follow_button"), {"target_user_pk": self.test_user_followed.pk})
        with self.subTest(response=response):
            self.assertEqual(response.status_code, 200)
        with self.subTest(response=response):
            self.assertEqual(response.json()["method"], "follow")
        with self.subTest(response=response):
            self.assertTrue(self.tester_user.following.filter(pk=self.test_user_followed.pk).exists())
        with self.subTest(response=response):
            self.assertEqual(response.json()["follower_count"], 1)

    def test_user_is_following_target_user(self):
        self.client.force_login(self.tester_user)
        self.tester_user.following.add(self.test_user_followed)
        response = self.client.post(reverse("follow_button"), {"target_user_pk": self.test_user_followed.pk})
        self.assertEqual(response.json()["method"], "unfollow")
        self.assertFalse(self.tester_user.following.filter(pk=self.test_user_followed.pk).exists())
        self.assertEqual(response.json()["follower_count"], 0)

    def test_with_not_exist_user(self):
        self.client.force_login(self.tester_user)
        response = self.client.post(reverse("follow_button"), {"target_user_pk": 100})
        self.assertEqual(response.status_code, 404)

    def test_with_request_user_itself(self):
        self.client.force_login(self.tester_user)
        response = self.client.post(reverse("follow_button"), {"target_user_pk": self.tester_user.pk})
        self.assertEqual(response.status_code, 400)
