import math

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.forms import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from punkweb_bb.models import (
    Category,
    Post,
    Shout,
    Subcategory,
    Thread,
    profile_image_upload_to,
)
from punkweb_bb.response import htmx_redirect

User = get_user_model()


class HTMXRedirectTestCase(TestCase):
    def test_htmx_redirect(self):
        response = htmx_redirect("/")

        self.assertEqual(response.headers["HX-Redirect"], "/")


class BoardProfileTestCase(TestCase):
    def test_is_created(self):
        user = User.objects.create_user(username="test", password="test")
        self.assertIsNotNone(user.profile)

    def test_profile_image_upload_to_path(self):
        user = User.objects.create_user(username="test", password="test")
        self.assertEqual(
            profile_image_upload_to(user.profile, "test.png"),
            f"punkweb_bb/board_profiles/{user.username}/image.png",
        )

    def test_str(self):
        user = User.objects.create_user(username="test", password="test")
        self.assertEqual(str(user.profile), "test")

    def test_post_count(self):
        user = User.objects.create_user(username="test", password="test")
        self.assertEqual(user.profile.post_count, 0)

        category = Category.objects.create(name="test")
        subcategory = Subcategory.objects.create(name="test", category=category)

        Thread.objects.create(
            subcategory=subcategory, user=user, title="test", content="test"
        )

        self.assertEqual(user.profile.post_count, 1)

        Post.objects.create(thread=Thread.objects.first(), user=user, content="test")

        self.assertEqual(user.profile.post_count, 2)

    def test_is_online(self):
        user = User.objects.create_user(username="test", password="test")
        self.assertEqual(user.profile.is_online, False)

        cache.set(f"profile_online_{user.profile.id}", timezone.now(), 60 * 5)

        self.assertEqual(user.profile.is_online, True)


class CategoryTestCase(TestCase):
    def test_str(self):
        category = Category.objects.create(name="test", order="0")
        self.assertEqual(str(category), "0. test")

    def test_get_absolute_url(self):
        category = Category.objects.create(name="test", slug="test")
        self.assertEqual(category.get_absolute_url(), "/#test.0")


class SubcategoryTestCase(TestCase):
    def test_str(self):
        category = Category.objects.create(name="test", order="0")
        subcategory = Subcategory.objects.create(
            name="test", category=category, order="0"
        )
        self.assertEqual(str(subcategory), "0. test > 0. test")

    def test_thread_count(self):
        user = User.objects.create_user(username="test", password="test")
        category = Category.objects.create(name="test")
        subcategory = Subcategory.objects.create(name="test", category=category)
        self.assertEqual(subcategory.thread_count, 0)

        Thread.objects.create(
            subcategory=subcategory, user=user, title="test", content="test"
        )

        self.assertEqual(subcategory.thread_count, 1)

    def test_post_count(self):
        user = User.objects.create_user(username="test", password="test")
        category = Category.objects.create(name="test")
        subcategory = Subcategory.objects.create(name="test", category=category)
        thread = Thread.objects.create(
            subcategory=subcategory, user=user, title="test", content="test"
        )
        self.assertEqual(subcategory.post_count, 0)

        Post.objects.create(thread=thread, user=user, content="test")

        self.assertEqual(subcategory.post_count, 1)

    def test_latest_thread(self):
        user = User.objects.create_user(username="test", password="test")
        category = Category.objects.create(name="test")
        subcategory = Subcategory.objects.create(name="test", category=category)
        self.assertIsNone(subcategory.latest_thread)

        thread_1 = Thread.objects.create(
            subcategory=subcategory, user=user, title="test", content="test"
        )

        self.assertEqual(subcategory.latest_thread, thread_1)

        thread_2 = Thread.objects.create(
            subcategory=subcategory, user=user, title="test", content="test"
        )

        self.assertEqual(subcategory.latest_thread, thread_2)

    def test_get_absolute_url(self):
        category = Category.objects.create(name="test", slug="test")
        subcategory = Subcategory.objects.create(
            category=category, name="test", slug="test"
        )
        self.assertEqual(subcategory.get_absolute_url(), "/subcategory/test/")


class ThreadTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.category = Category.objects.create(name="test")
        self.subcategory = Subcategory.objects.create(
            name="test", category=self.category, slug="test"
        )

    def test_thread_str(self):
        thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        self.assertEqual(str(thread), "test")

    def test_post_count(self):
        thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )

        self.assertEqual(thread.post_count, 0)

        Post.objects.create(thread=thread, user=self.user, content="test")

        self.assertEqual(thread.post_count, 1)

    def test_latest_post(self):
        thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        self.assertIsNone(thread.latest_post)

        post_1 = Post.objects.create(thread=thread, user=self.user, content="test")

        self.assertEqual(thread.latest_post, post_1)

        post_2 = Post.objects.create(thread=thread, user=self.user, content="test")

        self.assertEqual(thread.latest_post, post_2)

    def test_last_post_created_at(self):
        thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        initial_last_post_created_at = thread.last_post_created_at
        Post.objects.create(thread=thread, user=self.user, content="test")
        new_last_post_created_at = thread.last_post_created_at

        self.assertGreater(new_last_post_created_at, initial_last_post_created_at)

    def test_is_closed(self):
        thread = Thread.objects.create(
            subcategory=self.subcategory,
            user=self.user,
            title="test",
            content="test",
            is_closed=True,
        )
        self.assertEqual(thread.is_closed, True)

        post = Post(
            thread=thread,
            user=self.user,
            content="test",
        )

        self.assertRaises(ValidationError, post.save)

    def test_is_pinned(self):
        thread = Thread.objects.create(
            subcategory=self.subcategory,
            user=self.user,
            title="test1",
            content="test1",
            is_pinned=True,
        )
        self.assertEqual(thread.is_pinned, True)

        Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test2", content="test2"
        )

        threads = Thread.objects.all()

        self.assertEqual(threads[0], thread)

    def test_bump(self):
        thread1 = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test1", content="test1"
        )
        Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test2", content="test2"
        )
        Post.objects.create(thread=thread1, user=self.user, content="test1")
        threads = Thread.objects.all()

        self.assertEqual(threads[0], thread1)

    def test_get_absolute_url(self):
        thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        self.assertEqual(thread.get_absolute_url(), f"/thread/{thread.id}/")


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.category = Category.objects.create(name="test")
        self.subcategory = Subcategory.objects.create(
            name="test", category=self.category
        )
        self.thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )

    def test_str(self):
        post = Post.objects.create(thread=self.thread, user=self.user, content="test")
        self.assertEqual(str(post), f"{post.thread} > {post.user} > {post.created_at}")

    def test_index(self):
        post_1 = Post.objects.create(thread=self.thread, user=self.user, content="test")
        post_2 = Post.objects.create(thread=self.thread, user=self.user, content="test")
        post_3 = Post.objects.create(thread=self.thread, user=self.user, content="test")

        self.assertEqual(post_1.index, 1)
        self.assertEqual(post_2.index, 2)
        self.assertEqual(post_3.index, 3)

    def test_page_number(self):
        for i in range(1, 21):
            post = Post.objects.create(
                thread=self.thread, user=self.user, content=f"test {i}"
            )
            self.assertEqual(post.page_number, math.ceil(i / 10))

    def test_get_absolute_url(self):
        post = Post.objects.create(thread=self.thread, user=self.user, content="test")
        self.assertEqual(
            post.get_absolute_url(),
            f"/thread/{post.thread.id}/?page={post.page_number}#post-{post.id}",
        )


class ShoutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")

    def test_str(self):
        shout = Shout.objects.create(user=self.user, content="test")
        self.assertEqual(str(shout), f"{shout.user} > {shout.created_at}")


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("punkweb_bb:index")
        self.user = User.objects.create(username="test", password="test")
        self.staff_user = User.objects.create(
            username="staff", password="staff", is_staff=True
        )

    def test_users_online(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["users_online"]), 0)

        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(len(response.context["users_online"]), 1)

    def test_staff_online(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["staff_online"]), 0)

        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)

        self.assertEqual(len(response.context["staff_online"]), 1)

    def test_newest_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["newest_user"], self.staff_user)

    def test_users_count(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["users"].count(), 2)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("punkweb_bb:login")
        self.user = User.objects.create_user(username="test", password="test")

    def test_redirect_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse("punkweb_bb:index"))

    def test_login(self):
        response = self.client.post(
            self.url, {"username": "test", "password": "test"}, follow=True
        )

        self.assertRedirects(response, reverse("punkweb_bb:index"))
        self.assertTrue(response.context["user"].is_authenticated)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("punkweb_bb:logout")
        self.user = User.objects.create_user(username="test", password="test")

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, reverse("punkweb_bb:login"))
        self.assertFalse(response.context["user"].is_authenticated)


class SignupViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("punkweb_bb:signup")
        self.user = User.objects.create_user(username="test1", password="test")

    def test_redirect_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse("punkweb_bb:index"))

    def test_signup(self):
        response = self.client.post(
            self.url,
            {
                "username": "test2",
                "password1": "needsmorecomplexity",
                "password2": "needsmorecomplexity",
            },
        )

        self.assertRedirects(response, reverse("punkweb_bb:login"))


class SettingsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("punkweb_bb:settings")
        self.user = User.objects.create_user(username="test", password="test")

    def test_redirect_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('punkweb_bb:login')}?next={self.url}")

    def test_settings(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.client.post(
            self.url,
            {
                "signature": "[b]test[/b]",
            },
        )

        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile._signature_rendered, "<strong>test</strong>")

        self.assertEqual(response.status_code, 200)


class ThreadCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")
        self.category = Category.objects.create(name="test")
        self.subcategory = Subcategory.objects.create(
            name="test", category=self.category, slug="test"
        )
        self.staff_subcategory = Subcategory.objects.create(
            name="staff", category=self.category, slug="staff", staff_post_only=True
        )
        self.url = reverse("punkweb_bb:thread_create", args=[self.subcategory.slug])
        self.staff_only_url = reverse(
            "punkweb_bb:thread_create", args=[self.staff_subcategory.slug]
        )

    def test_redirect_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('punkweb_bb:login')}?next={self.url}")

    def test_thread_create(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.url,
            {
                "title": "test",
                "content": "test",
            },
            follow=True,
        )

        new_thread = Thread.objects.first()

        self.assertRedirects(response, new_thread.get_absolute_url())
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(new_thread.user, self.user)
        self.assertEqual(new_thread.subcategory, self.subcategory)

    def test_thread_create_staff_post_only(self):
        self.client.force_login(self.user)
        response = self.client.get(self.staff_only_url)

        self.assertRedirects(response, self.staff_subcategory.get_absolute_url())


class ThreadViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")
        self.category = Category.objects.create(name="test")
        self.subcategory = Subcategory.objects.create(
            name="test", category=self.category, slug="test"
        )
        self.thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        self.url = reverse("punkweb_bb:thread", args=[self.thread.id])

    def test_view_count(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["thread"].view_count, 1)

        # ensure that the view count does not increase when viewed again from the same session

        response = self.client.get(self.url)
        self.assertEqual(response.context["thread"].view_count, 1)


class ThreadUpdateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")
        self.other_user = User.objects.create_user(username="other", password="other")
        self.category = Category.objects.create(name="test")
        self.subcategory = Subcategory.objects.create(
            name="test", category=self.category, slug="test"
        )
        self.thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        self.url = reverse("punkweb_bb:thread_update", args=[self.thread.id])

    def test_redirect_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('punkweb_bb:login')}?next={self.url}")

    def test_is_author(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_thread_update(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.url,
            {
                "title": "edit",
                "content": "edit",
            },
            follow=True,
        )

        self.assertRedirects(response, self.thread.get_absolute_url())
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, "edit")
        self.assertEqual(self.thread._content_rendered, "edit")


class ThreadDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")
        self.other_user = User.objects.create_user(username="other", password="other")
        self.category = Category.objects.create(name="test")
        self.subcategory = Subcategory.objects.create(
            name="test", category=self.category, slug="test"
        )
        self.thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        self.url = reverse("punkweb_bb:thread_delete", args=[self.thread.id])

    def test_redirect_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('punkweb_bb:login')}?next={self.url}")

    def test_is_author(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_thread_delete(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        response = self.client.delete(self.url, follow=True)

        self.assertEqual(
            response.headers["HX-Redirect"], self.subcategory.get_absolute_url()
        )
        self.assertEqual(Thread.objects.count(), 0)


class PostCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")
        self.category = Category.objects.create(name="test")
        self.subcategory = Subcategory.objects.create(
            name="test", category=self.category, slug="test"
        )
        self.thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        self.url = reverse("punkweb_bb:post_create", args=[self.thread.id])

    def test_redirect_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('punkweb_bb:login')}?next={self.url}")

    def test_post_create(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {
                "content": "test",
            },
            follow=True,
        )

        new_post = Post.objects.first()

        self.assertRedirects(response, new_post.get_absolute_url())
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(new_post.user, self.user)
        self.assertEqual(new_post.thread, self.thread)


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")
        self.other_user = User.objects.create_user(username="other", password="other")
        self.category = Category.objects.create(name="test")
        self.subcategory = Subcategory.objects.create(
            name="test", category=self.category, slug="test"
        )
        self.thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        self.post = Post.objects.create(
            thread=self.thread, user=self.user, content="test"
        )
        self.url = reverse("punkweb_bb:post_update", args=[self.post.id])

    def test_redirect_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('punkweb_bb:login')}?next={self.url}")

    def test_is_author(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_update(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.url,
            {
                "content": "edit",
            },
            follow=True,
        )

        self.assertRedirects(response, self.post.get_absolute_url())
        self.post.refresh_from_db()
        self.assertEqual(self.post._content_rendered, "edit")


class PostDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")
        self.other_user = User.objects.create_user(username="other", password="other")
        self.category = Category.objects.create(name="test")
        self.subcategory = Subcategory.objects.create(
            name="test", category=self.category, slug="test"
        )
        self.thread = Thread.objects.create(
            subcategory=self.subcategory, user=self.user, title="test", content="test"
        )
        self.post = Post.objects.create(
            thread=self.thread, user=self.user, content="test"
        )
        self.url = reverse("punkweb_bb:post_delete", args=[self.post.id])

    def test_redirect_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('punkweb_bb:login')}?next={self.url}")

    def test_is_author(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        response = self.client.delete(self.url, follow=True)

        self.assertEqual(
            response.headers["HX-Redirect"], self.thread.get_absolute_url()
        )
        self.assertEqual(Post.objects.count(), 0)


class ShoutCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")
        self.url = reverse("punkweb_bb:shout_create")

    def test_unauthenticated(self):
        response = self.client.get(self.url)

        self.client.post(
            self.url,
            {
                "content": "test",
            },
        )

        self.assertEqual(Shout.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_shout_create(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {
                "content": "test",
            },
            follow=True,
        )

        self.assertEqual(Shout.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
