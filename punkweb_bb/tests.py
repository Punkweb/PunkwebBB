from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import BoardProfile, Category, Post, Shout, Subcategory, Thread

User = get_user_model()


class BoardProfileTestCase(TestCase):
    def test_board_profile_is_created(self):
        user = User.objects.create_user(username="test", password="test")
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.user, user)
        self.assertEqual(user.profile.user.username, "test")
        self.assertEqual(user.profile.user.is_active, True)

    def test_board_profile_str(self):
        user = User.objects.create_user(username="test", password="test")
        self.assertEqual(str(user.profile), "test")

    def test_board_profile_post_count(self):
        user = User.objects.create_user(username="test", password="test")
        self.assertEqual(user.profile.post_count(), 0)

        category = Category.objects.create(name="test")
        subcategory = Subcategory.objects.create(name="test", category=category)

        Thread.objects.create(
            subcategory=subcategory, user=user, title="test", content="test"
        )

        self.assertEqual(user.profile.post_count(), 1)

        Post.objects.create(thread=Thread.objects.first(), user=user, content="test")

        self.assertEqual(user.profile.post_count(), 2)


class CategoryTestCase(TestCase):
    def test_category_str(self):
        category = Category.objects.create(name="test", order="0")
        self.assertEqual(str(category), "0. test")


class SubcategoryTestCase(TestCase):
    def test_subcategory_str(self):
        category = Category.objects.create(name="test", order="0")
        subcategory = Subcategory.objects.create(
            name="test", category=category, order="0"
        )
        self.assertEqual(str(subcategory), "0. test > 0. test")

    def test_subcategory_thread_count(self):
        user = User.objects.create_user(username="test", password="test")
        category = Category.objects.create(name="test")
        subcategory = Subcategory.objects.create(name="test", category=category)
        self.assertEqual(subcategory.thread_count(), 0)

        Thread.objects.create(
            subcategory=subcategory, user=user, title="test", content="test"
        )

        self.assertEqual(subcategory.thread_count(), 1)

    def test_subcategory_post_count(self):
        user = User.objects.create_user(username="test", password="test")
        category = Category.objects.create(name="test")
        subcategory = Subcategory.objects.create(name="test", category=category)
        thread = Thread.objects.create(
            subcategory=subcategory, user=user, title="test", content="test"
        )
        self.assertEqual(subcategory.post_count(), 0)

        Post.objects.create(thread=thread, user=user, content="test")

        self.assertEqual(subcategory.post_count(), 1)


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

        self.assertEqual(thread.post_count(), 0)

        Post.objects.create(thread=thread, user=self.user, content="test")

        self.assertEqual(thread.post_count(), 1)


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

    def test_post_str(self):
        post = Post.objects.create(thread=self.thread, user=self.user, content="test")
        self.assertEqual(str(post), f"{post.thread} > {post.user} > {post.created_at}")


class ShoutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")

    def test_shout_str(self):
        shout = Shout.objects.create(user=self.user, content="test")
        self.assertEqual(str(shout), f"{shout.user} > {shout.created_at}")
