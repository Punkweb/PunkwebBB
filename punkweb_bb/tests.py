import math

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
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
            name="test", category=self.category
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
