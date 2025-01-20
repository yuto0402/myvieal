from django.test import TestCase
from django.urls import reverse
from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from myvieal.forms import *

# Create your tests here.
class MovieTests(TestCase):
  def setUp(self):
    self.user = CustomUser.objects.create_user(username="testuser", email="test@example.com", password="password")
    self.client.login(username="testuser", password="password")
    self.tag = Tag.objects.create(name="Action", genre="movies", created_by=self.user)
    self.video = SimpleUploadedFile("test_video.mp4", b"dummy data", content_type="video/mp4")
    self.movie = Movie.objects.create(
      title="Test Movie",
      explanation='Test',
      movie_file=self.video,
      created_by=self.user,
    )
    self.movie.tag_list.add(self.tag)

  def test_top(self):
    response = self.client.get(reverse('top'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'myvieal/top.html')
    self.assertContains(response, 'test')

  def test_movie_top_user_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("top"))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('top')}", status_code=302, target_status_code=200)

  def test_movie_create(self):
    response = self.client.get(reverse('MovieCreate'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'myvieal/create.html')
    self.assertIsInstance(response.context["form"], MovieForm)

  def test_movie_create_submit(self):
    new_video = SimpleUploadedFile("new_video.mp4", b"new dummy data", content_type="video/mp4")
    response = self.client.post(
        reverse("MovieCreate"),
        {
            "title": "New Movie",
            "explanation": "This is a new movie.",
            "movie_file": new_video,
            "tag_list": [self.tag.id],
            "name": "Test name",
            "address": "Test Address",
            "place_id": "Test PlaceId"
        },
        format="multipart",
    )
    self.assertEqual(response.status_code, 302)
    new_movie = Movie.objects.get(title="New Movie")
    self.assertEqual(new_movie.explanation, "This is a new movie.")

  def test_movie_create_user_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("MovieCreate"))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('MovieCreate')}", status_code=302, target_status_code=200)

  def test_movie_edit(self):
    response = self.client.get(reverse("MovieEdit", kwargs={"pk": self.movie.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'myvieal/edit.html')
    self.assertIsInstance(response.context["form"], MovieEditForm)
    form = response.context["form"]
    self.assertEqual(form.initial["title"], self.movie.title)

  def test_movie_edit_submit(self):
    updated_video = SimpleUploadedFile("updated_video.mp4", b"updated dummy data", content_type="video/mp4")
    response = self.client.post(
      reverse("MovieEdit", kwargs={"pk": self.movie.pk}),
        {
            "title": "Updated Movie",
            "explanation": "Updated explanation.",
            "movie_file": updated_video,
            "tag_list": [self.tag.id],
            "name": "Updated name",
            "address": "Updated Address",
            "place_id": "Updated PlaceId"
        },
    )
    self.assertEqual(response.status_code, 302)
    self.movie.refresh_from_db()
    self.assertEqual(self.movie.title, "Updated Movie")
    self.assertEqual(self.movie.explanation, "Updated explanation.")

  def test_movie_edit_user_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("MovieEdit", kwargs={"pk": self.movie.pk}))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse("MovieEdit", kwargs={"pk": self.movie.pk})}", status_code=302, target_status_code=200)

  def test_movie_detail(self):
    response = self.client.get(reverse("MovieDetail", kwargs={"pk": self.movie.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "myvieal/detail.html")
    self.assertContains(response, "Test Movie")
    self.movie.refresh_from_db()
    self.assertEqual(self.movie.number_of_views, 1)

  def test_movie_detail_user_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("MovieDetail", kwargs={"pk": self.movie.pk}))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse("MovieDetail", kwargs={"pk": self.movie.pk})}", status_code=302, target_status_code=200)

  def test_movie_delete(self):
    response = self.client.get(reverse("MovieDelete", kwargs={"pk": self.movie.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'myvieal/delete.html')

  def test_movie_delete_submit(self):
    response = self.client.post(reverse("MovieDelete", kwargs={"pk": self.movie.pk}))
    self.assertEqual(response.status_code, 302)
    self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())

  def test_movie_delete_user_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("MovieDelete", kwargs={"pk": self.movie.pk}))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse("MovieDelete", kwargs={"pk": self.movie.pk})}", status_code=302, target_status_code=200)

class MapHistoryViewTest(TestCase):
  def setUp(self):
    self.user = CustomUser.objects.create_user(username="testuser", email="test@example.com", password="password")
    self.client.login(username="testuser", password="password")
    self.map_history = MapHistory.objects.create(
      map_searched_by=self.user,
      place_id="test_place_id",
      name="Test Name",
      address="Test Address",
      map_searched_at=timezone.now(),
    )

  def test_map_history(self):
    response = self.client.get(reverse('MapHistory'))
    self.assertTemplateUsed(response, 'myvieal/map_history.html')
    self.assertEqual(len(response.context['map_histories']), 1)
    self.assertEqual(response.context['map_histories'][0].place_id, self.map_history.place_id)
    self.assertEqual(response.context['map_histories'][0].name, self.map_history.name)
    self.assertEqual(response.context['map_histories'][0].address, self.map_history.address)

  def test_map_history_user_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("MapHistory"))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('MapHistory')}", status_code=302, target_status_code=200)

class MapResultViewTest(TestCase):
  def setUp(self):
    self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
    self.client.login(username="testuser", password="testpassword")
    self.tag = Tag.objects.create(name="Action", genre="movies", created_by=self.user)
    self.movie = Movie.objects.create(
      created_by=self.user,
      title="Test Movie",
      explanation="Test Explanation",
      place_id="test_place_id",
      name="Test Name",
      address="Test Address",
      movie_file=SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4"),
    )
    self.place_id = "input_place_id"
    self.name = "Input Name"
    self.address = "Input Address"
    self.movie.tag_list.add(self.tag)

  def test_map_history_creation(self):
    initial_count = MapHistory.objects.count()
    response = self.client.get(reverse('MapResult'), {'placeId': self.place_id, 'name': self.name, 'address': self.address})
    self.assertEqual(MapHistory.objects.count(), initial_count + 1)
    map_history = MapHistory.objects.last()
    self.assertEqual(map_history.map_searched_by, self.user)
    self.assertEqual(map_history.place_id, self.place_id)
    self.assertEqual(map_history.name, self.name)
    self.assertEqual(map_history.address, self.address)
    self.assertTrue(map_history.map_searched_at <= timezone.now())

  def test_map_result(self):
    response = self.client.get(reverse('MapResult'), {'placeId': 'test_place_id', 'name': 'Test Name'})
    self.assertTemplateUsed(response, 'myvieal/map.html')
    self.assertEqual(len(response.context['movies']), 1)
    self.assertEqual(response.context['movies'][0].title, self.movie.title)
    self.assertIn(self.tag, response.context['tags'])

  def test_map_result_order_by_created_at(self):
    response = self.client.get(reverse('MapResult'), {'placeId': 'test_place_id', 'display_order': 'created_at'})
    self.assertEqual(response.context['is_searched_by_created_at'], True)

  def test_map_result_order_by_number_of_views(self):
    response = self.client.get(reverse('MapResult'), {'placeId': 'test_place_id', 'display_order': 'number_of_views'})
    self.assertEqual(response.context['is_searched_by_numbers_of_views'], True)

  def test_map_result_order_by_related(self):
    response = self.client.get(reverse('MapResult'), {'placeId': 'test_place_id', 'display_order': 'related'})
    self.assertEqual(response.context['is_searched_by_related'], True)

  def test_map_result_no_order(self):
    response = self.client.get(reverse('MapResult'), {'placeId': 'test_place_id', 'name': 'Test Name'})
    self.assertEqual(len(response.context['movies']), 1)
    self.assertEqual(response.context['movies'][0].title, self.movie.title)

  def test_map_result_user_not_logged_in(self):
    self.client.logout()
    response = self.client.get(reverse("MapResult"))
    self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('MapResult')}", status_code=302, target_status_code=200)
