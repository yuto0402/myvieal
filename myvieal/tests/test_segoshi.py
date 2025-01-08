from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from myvieal.models import Movie


def tool_request_by_post(test_case, url_name):
    """test_caseとurl_nameを受け取り、test_caseのclientを使ってurl_nameと対応するURLにpostリクエストを送り、405エラーになることを検証する"""
    response = test_case.client.post(reverse(url_name))
    test_case.assertEqual(response.status_code, 405)


class LibraryTests(TestCase):
    def setUp(self):
        self.tester_user = CustomUser.objects.create_user("tester")

    def test_request_by_post(self):
        self.client.force_login(self.tester_user)
        response = self.client.post(reverse("library"))
        self.assertEqual(response.status_code, 405)

    def test_user_is_logined(self):
        self.client.force_login(self.tester_user)
        response = self.client.get(reverse("library"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myvieal/library.html")

    def test_user_is_not_logined(self):
        response = self.client.get(reverse("library"))
        self.assertRedirects(
            response, f"{reverse("account_login")}?next={reverse("library")}", status_code=302, target_status_code=200
        )

    def test_following_user_queryset(self):
        self.client.force_login(self.tester_user)
        test_user_followed = CustomUser.objects.create_user("test_followed")
        self.tester_user.following.add(test_user_followed)
        response = self.client.get(reverse("library"))
        self.assertQuerySetEqual(response.context["object_list"], self.tester_user.following.all())

    def test_movie_like_queryset(self):
        self.client.force_login(self.tester_user)

        test_movie = Movie.objects.create(title="test_title", movie_file="test.mp4", created_by=self.tester_user)

        self.tester_user.movie_like.add(test_movie)

        response = self.client.get(reverse("library"))
        self.assertQuerySetEqual(response.context["movies"], self.tester_user.movie_like.all())


class FavoriteButtonTest(TestCase):
    def setUp(self):
        self.tester_user = CustomUser.objects.create_user("tester")
        self.test_movie = Movie.objects.create(title="test_title", movie_file="test.mp4", created_by=self.tester_user)

    def test_request_by_get(self):
        self.client.force_login(self.tester_user)
        response = self.client.get(reverse("favorite_button"))
        self.assertEqual(response.status_code, 405)

    def test_user_is_not_logined(self):
        response = self.client.post(reverse("favorite_button"))
        self.assertRedirects(
            response,
            f"{reverse("account_login")}?next={reverse("favorite_button")}",
            status_code=302,
            target_status_code=200,
        )

    def test_user_is_not_favorite_target_movie(self):
        self.client.force_login(self.tester_user)
        response = self.client.post(reverse("favorite_button"), {"target_movie_pk": self.test_movie.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["method"], "favorite")
        self.assertTrue(self.tester_user.movie_like.filter(pk=self.test_movie.pk).exists())

    def test_user_is_favorite_target_movie(self):
        self.client.force_login(self.tester_user)
        self.tester_user.movie_like.add(self.test_movie)
        response = self.client.post(reverse("favorite_button"), {"target_movie_pk": self.test_movie.pk})
        self.assertEqual(response.json()["method"], "unfavorite")
        self.assertFalse(self.tester_user.movie_like.filter(pk=self.test_movie.pk).exists())

    def test_with_not_exist_movie(self):
        self.client.force_login(self.tester_user)
        response = self.client.post(reverse("favorite_button"), {"target_movie_pk": 100})
        self.assertEqual(response.status_code, 404)


class PrivacyPolicyTest(TestCase):
    def test_request_by_post(self):
        return tool_request_by_post(self, "privacy_policy")

    def test_response_status_code_is_200_and_use_expected_template(self):
        response = self.client.get(reverse("privacy_policy"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myvieal/privacy_policy.html")


class TermOfUseTest(TestCase):
    def test_request_by_post(self):
        return tool_request_by_post(self, "term_of_use")

    def test_response_status_code_is_200_and_use_expected_template(self):
        response = self.client.get(reverse("term_of_use"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myvieal/term_of_use.html")
