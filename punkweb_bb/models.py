from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe
from precise_bbcode.fields import BBCodeTextField

from .mixins import UUIDPrimaryKeyMixin, TimestampMixin


User = get_user_model()


class BoardProfile(UUIDPrimaryKeyMixin, TimestampMixin):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    signature = BBCodeTextField(max_length=1024, blank=True, null=True)

    class Meta:
        ordering = [
            "user__username",
        ]

    def __str__(self):
        return self.user.username

    def rendered_signature(self):
        return mark_safe(self.signature.rendered)


class Category(UUIDPrimaryKeyMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1024, unique=True)
    description = BBCodeTextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = [
            "order",
        ]

    def __str__(self):
        return f"{self.order}. {self.name}"


class Subcategory(UUIDPrimaryKeyMixin, TimestampMixin):
    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1024, unique=True)
    description = BBCodeTextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"
        ordering = [
            "category__order",
            "order",
        ]

    def __str__(self):
        return f"{self.category} > {self.order}. {self.name}"

    def thread_count(self):
        return self.threads.count()

    def post_count(self):
        return sum([thread.post_count() for thread in self.threads.all()])


class Thread(UUIDPrimaryKeyMixin, TimestampMixin):
    subcategory = models.ForeignKey(
        Subcategory, related_name="threads", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="threads", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = BBCodeTextField()

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return f"{self.title}"

    def post_count(self):
        return self.posts.count()


class Post(UUIDPrimaryKeyMixin, TimestampMixin):
    thread = models.ForeignKey(Thread, related_name="posts", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = BBCodeTextField()

    class Meta:
        ordering = [
            "created_at",
        ]

    def __str__(self):
        return f"{self.thread} > {self.user} > {self.created_at}"
