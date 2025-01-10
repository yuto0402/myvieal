from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import CustomUser
from myvieal.models import Movie


class RedirectIfAuthenticatedTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")

    # account_signup
    def test_signup_page_for_anonymous_user(self):
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup_email.html")

    def test_signup_page_for_authenticated_user(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("account_signup"))
        self.assertRedirects(response, reverse("top"))

    # account_signup_email_confirmation
    def test_signup_email_confirmation_page_for_authenticated_user(self):
        session = self.client.session
        session["signup_email"] = "testuser@st.kyoto-u.ac.jp"
        session.save()
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("account_signup_email_confirmation"))
        self.assertRedirects(response, reverse("top"))

    # account_login
    def test_login_page_for_anonymous_user(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

    def test_login_page_for_authenticated_user(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("account_login"))
        self.assertRedirects(response, reverse("top"))


class Signup(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuserx@st.kyoto-u.ac.jp", is_active=False
        )

    def test_new_signup_email(self):
        response = self.client.post(reverse("account_signup"), {"email": "testuser@st.kyoto-u.ac.jp"})
        self.assertTrue(self.client.session.get("signup_email"), self.client.session.get("email_verification_code"))
        self.assertRedirects(response, reverse("account_signup_email_confirmation"))

    def test_previous_signup_email(self):
        """
        self.client.session["signup_email"] = "testuser@st.kyoto-u.ac.jp"
        self.client.session.save()
        は動作しなくて、
        session = self.client.session
        session["signup_email"] = "testuser@st.kyoto-u.ac.jp"
        session.save()
        のように一回変数を咬ますと動作する(なんで?!?!?!)
        """
        session = self.client.session
        session["signup_email"] = "testuser@st.kyoto-u.ac.jp"
        session.save()
        response = self.client.get(reverse("account_signup"))
        self.assertRedirects(response, reverse("account_signup_email_confirmation"))

    def test_authenticated_signup_email(self):
        session = self.client.session
        session["signup_email_true"] = "testuserx@st.kyoto-u.ac.jp"
        session.save()
        # test1
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup_email.html")
        # test2
        response = self.client.post(reverse("account_signup"), {"email": "testuserx@st.kyoto-u.ac.jp"})
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        self.assertRedirects(response, reverse("account_signup_true", kwargs={"uidb64": uid, "token": token}))

    def test_email_confirmation(self):
        # test1
        response = self.client.get(reverse("account_signup_email_confirmation"))
        self.assertRedirects(response, reverse("account_signup"))
        # test2
        session = self.client.session
        session["signup_email"] = "testuser@st.kyoto-u.ac.jp"
        session.save()
        response = self.client.post(reverse("account_signup_email_confirmation"), {"email_verification_code": 0000})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup_email_confirmation.html")
        self.assertContains(response, "Invalid verification code")
        # test3, 4
        session = self.client.session
        session.clear()
        session["signup_email"] = "testuser@st.kyoto-u.ac.jp"
        session["email_verification_code"] = "1111"
        session.save()
        for _ in range(2):
            response = self.client.post(
                reverse("account_signup_email_confirmation"), {"email_verification_code": "0000"}
            )
            self.assertTrue(self.client.session.get("signup_email"))
            self.assertTrue(self.client.session.get("email_verification_code"))
            self.assertTrue(self.client.session.get("attempts"))
        response = self.client.post(
            reverse("account_signup_email_confirmation"), {"email_verification_code": "0000"}, follow=True
        )
        self.assertFalse(self.client.session.get("signup_email"))
        self.assertFalse(self.client.session.get("email_verification_code"))
        self.assertFalse(self.client.session.get("attempts"))
        self.assertRedirects(response, reverse("account_signup"))
        # test5
        session = self.client.session
        session.clear()
        session["signup_email"] = "testuser@st.kyoto-u.ac.jp"
        session["email_verification_code"] = "1111"
        session.save()
        response = self.client.post(reverse("account_signup_email_confirmation"), {"email_verification_code": "1111"})
        false_user = CustomUser.objects.get(email="testuser@st.kyoto-u.ac.jp")  # dummy0
        self.assertFalse(self.client.session.get("signup_email"))
        self.assertFalse(self.client.session.get("email_verification_code"))
        self.assertFalse(self.client.session.get("attempts"))
        self.assertTrue(self.client.session.get("signup_email_true"))
        uid = urlsafe_base64_encode(force_bytes(false_user.pk))
        token = default_token_generator.make_token(false_user)
        self.assertRedirects(response, reverse("account_signup_true", kwargs={"uidb64": uid, "token": token}))
        # test6, 7
        session = self.client.session
        session["signup_email"] = "testuser@st.kyoto-u.ac.jp"
        session["email_verification_code"] = "1111"
        session["signup_email_true"] = "testuserx@st.kyoto-u.ac.jp"
        session.save()  # signup_email_true session was deleted, but dummy0 still alive
        response = self.client.post(reverse("account_signup_email_confirmation"), {"email_verification_code": "1111"})
        self.assertNotIn("testuser", CustomUser.objects.all())

    def test_true_signup(self):
        # test1
        session = self.client.session
        session["signup_email_true"] = "testuserx@st.kyoto-u.ac.jp"
        session.save()
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.post(
            reverse("account_signup_true", kwargs={"uidb64": uid, "token": token}),
            {"username": "dummy", "password1": "testpwd123", "password2": "testpwd123", "privacy-policy": "on"},
        )
        self.assertRedirects(response, reverse("top"))
        # test2
        session = self.client.session
        session.clear()
        session.save()
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.post(
            reverse("account_signup_true", kwargs={"uidb64": uid, "token": token}),
            {"username": "dummy", "password1": "password123", "password2": "password123", "privacy-policy": "on"},
        )
        self.assertRedirects(response, reverse("account_signup"))


class Login(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="testuser@st.kyoto-u.ac.jp"
        )

    def test_login(self):
        response = self.client.post(
            reverse("account_login"), {"login": "testuser@st.kyoto-u.ac.jp", "password": "password123"}
        )
        self.assertRedirects(response, reverse("top"))


class PasswordReset(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="testuser@st.kyoto-u.ac.jp"
        )

    def test_password_reset_get(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/password_reset.html")

    def test_password_reset_application(self):
        response = self.client.post(reverse("password_reset"), {"email": "testuser@st.kyoto-u.ac.jp"})
        self.assertRedirects(response, reverse("password_reset_done"))

    def test_password_reset_email_verification(self):
        # test1
        session = self.client.session
        session["password_reset_email"] = "testuser@st.kyoto-u.ac.jp"
        session.save()
        response = self.client.post(reverse("password_reset_done"), {"verification_code": "0000"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/password_reset_done.html")
        self.assertContains(response, "Invalid verification code")
        # test2
        session = self.client.session
        session.clear()
        session["password_reset_email"] = "testuser@st.kyoto-u.ac.jp"
        session["verification_code"] = "1111"
        session.save()
        response = self.client.post(reverse("password_reset_done"), {"verification_code": "1111"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/password_reset_from_key.html")


class ResendMail(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="testuserx@st.kyoto-u.ac.jp"
        )

    def test_405(self):
        response = self.client.get(reverse("resend"))
        self.assertEqual(response.status_code, 405)
        response = self.client.get(reverse("resend_password"))
        self.assertEqual(response.status_code, 405)
        response = self.client.get(reverse("resend_email"))
        self.assertEqual(response.status_code, 405)

    def test_resend(self):
        # test1
        response = self.client.post(reverse("resend"))
        self.assertEqual(response.status_code, 400)
        # test2
        session = self.client.session
        session["signup_email"] = "testuser@st.kyoto-u.ac.jp"
        session["attempts"] = 2
        session.save()
        response = self.client.post(reverse("resend"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup_email_confirmation.html")
        self.assertTrue(self.client.session.get("email_verification_code"))
        self.assertFalse(self.client.session.get("attempts"))

    def test_resend_password(self):
        # test1
        response = self.client.post(reverse("resend_password"))
        self.assertEqual(response.status_code, 400)
        # test2
        session = self.client.session
        session["password_reset_email"] = "testuserx@st.kyoto-u.ac.jp"
        session.save()
        response = self.client.post(reverse("resend_password"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/password_reset_done.html")
        self.assertTrue(self.client.session.get("verification_code"))

    def test_resend_email(self):
        # test1
        response = self.client.post(reverse("resend_email"))
        self.assertEqual(response.status_code, 400)
        # test2
        session = self.client.session
        session["new_email"] = "testuser@st.kyoto-u.ac.jp"
        session["attempts"] = 2
        session.save()
        response = self.client.post(reverse("resend_email"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/email_change_confirmation.html")
        self.assertTrue(self.client.session.get("email_change_code"))
        self.assertFalse(self.client.session.get("attempts"))


class EmailChange(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="testuserx@st.kyoto-u.ac.jp"
        )

    def test_email_change_get(self):
        # test1
        response = self.client.get(reverse("EmailChange"), follow=True)
        self.assertTemplateUsed(response, "account/login.html")
        # test2
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("EmailChange"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/email_change.html")
        # test3
        session = self.client.session
        session["new_email"] = "testuser@st.kyoto-u.ac.jp"
        session.save()
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("EmailChange"))
        self.assertRedirects(response, reverse("EmailChangeConfirmation"))

    def test_email_change_application(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("EmailChange"), {"email": "testuser@st.kyoto-u.ac.jp"}, follow=True)
        self.assertRedirects(response, reverse("EmailChangeConfirmation"))
        self.assertTrue(self.client.session.get("new_email"), self.client.session.get("email_change_code"))

    def test_email_change_confirmation_get(self):
        # test1
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("EmailChangeConfirmation"))
        self.assertRedirects(response, reverse("EmailChange"))
        # test2
        session = self.client.session
        session["new_email"] = "testuser@st.kyoto-u.ac.jp"
        session.save()
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("EmailChangeConfirmation"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/email_change_confirmation.html")

    def test_email_change_confirmation_application(self):
        # test1
        session = self.client.session
        session["new_email"] = "testuser@st.kyoto-u.ac.jp"
        session["email_change_code"] = "1111"
        session.save()
        self.client.login(username="testuser", password="password123")
        for _ in range(2):
            response = self.client.post(reverse("EmailChangeConfirmation"), {"email_change_code": "0000"})
            self.assertTrue(self.client.session.get("new_email"))
            self.assertTrue(self.client.session.get("email_change_code"))
            self.assertTrue(self.client.session.get("attempts"))
        response = self.client.post(reverse("EmailChangeConfirmation"), {"email_change_code": "0000"})
        self.assertFalse(self.client.session.get("new_email"))
        self.assertFalse(self.client.session.get("email_change_code"))
        self.assertFalse(self.client.session.get("attempts"))
        self.assertRedirects(response, reverse("UserSetting"))
        # test2
        session = self.client.session
        session.clear()
        session["new_email"] = "testuser@st.kyoto-u.ac.jp"
        session["email_change_code"] = "1111"
        session["attempts"] = 2
        session.save()
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("EmailChangeConfirmation"), {"email_change_code": "1111"})
        user = CustomUser.objects.get(username="testuser")
        self.assertFalse(self.client.session.get("new_email"))
        self.assertFalse(self.client.session.get("email_change_code"))
        self.assertFalse(self.client.session.get("attempts"))
        self.assertRedirects(response, reverse("UserSetting"))
        self.assertEqual(user.email, "testuser@st.kyoto-u.ac.jp")
        self.assertNotEqual(user.email, "testuserx@st.kyoto-u.ac.jp")

    def test_session_initializer(self):
        # test1
        response = self.client.get(reverse("trickpath"))
        self.assertEqual(response.status_code, 405)
        # test2
        session = self.client.session
        session["new_email"] = "testuser@st.kyoto-u.ac.jp"
        session["email_change_code"] = "1111"
        session["attempts"] = 2
        session.save()
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("trickpath"))
        self.assertFalse(self.client.session.get("new_email"))
        self.assertFalse(self.client.session.get("email_change_code"))
        self.assertFalse(self.client.session.get("attempts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/setting.html")


class Comment(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="testuser@st.kyoto-u.ac.jp"
        )
        self.movie = Movie.objects.create(title="testmovie", movie_file="test.mp4", created_by=self.user)

    def test_comment_post(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("MovieDetail", kwargs={"pk": self.movie.pk}), {"content": "This is test."}, follow=True
        )
        self.assertTemplateUsed(response, "myvieal/detail.html")
        self.assertContains(response, "This is test.")
