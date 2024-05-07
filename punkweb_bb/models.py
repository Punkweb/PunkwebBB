import datetime
import math
import os

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils import timezone
from precise_bbcode.fields import BBCodeTextField

from punkweb_bb.mixins import TimestampMixin, UUIDPrimaryKeyMixin

User = get_user_model()


def profile_image_upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1]
    return f"punkweb_bb/board_profiles/{instance.user.username}/image{ext}"


class BoardProfile(UUIDPrimaryKeyMixin, TimestampMixin):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=profile_image_upload_to, blank=True, null=True)
    signature = BBCodeTextField(max_length=1024, blank=True, null=True)

    class Meta:
        ordering = ("user__username",)

    @property
    def is_online(self):
        last_seen = cache.get(f"profile_online_{self.id}")
        if last_seen:
            return timezone.now() < last_seen + datetime.timedelta(minutes=5)
        return False

    @property
    def post_count(self):
        return self.user.threads.count() + self.user.posts.count()

    def __str__(self):
        return self.user.username


class Category(UUIDPrimaryKeyMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1024, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ("order",)

    def __str__(self):
        return f"{self.order}. {self.name}"

    def get_absolute_url(self):
        index_url = reverse("punkweb_bb:index")
        return f"{index_url}#{self.slug}.{self.order}"


class Subcategory(UUIDPrimaryKeyMixin, TimestampMixin):
    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1024, unique=True)
    description = BBCodeTextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    staff_post_only = models.BooleanField(default=False)

    class Meta:
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"
        ordering = (
            "category__order",
            "order",
        )

    @property
    def thread_count(self):
        return self.threads.count()

    @property
    def post_count(self):
        return sum([thread.post_count for thread in self.threads.all()])

    @property
    def latest_thread(self):
        return self.threads.order_by("-last_post_created_at").first()

    def __str__(self):
        return f"{self.category} > {self.order}. {self.name}"

    def get_absolute_url(self):
        return reverse("punkweb_bb:subcategory", args=[self.slug])


class Thread(UUIDPrimaryKeyMixin, TimestampMixin):
    subcategory = models.ForeignKey(
        Subcategory, related_name="threads", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="threads", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = BBCodeTextField()
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    last_post_created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = (
            "subcategory",
            "-is_pinned",
            "-last_post_created_at",
        )

    def __str__(self):
        return f"{self.title}"

    @property
    def post_count(self):
        return self.posts.count()

    @property
    def latest_post(self):
        return self.posts.order_by("-created_at").first()

    def get_absolute_url(self):
        return reverse("punkweb_bb:thread", args=[self.id])


class Post(UUIDPrimaryKeyMixin, TimestampMixin):
    thread = models.ForeignKey(Thread, related_name="posts", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = BBCodeTextField()

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.thread} > {self.user} > {self.created_at}"

    @property
    def index(self):
        # Returns the index of the post in the thread, starting with 1

        qs = self.thread.posts.order_by("created_at")
        index = list(qs.values_list("id", flat=True)).index(self.id)
        return index + 1

    @property
    def page_number(self):
        return math.ceil(self.index / 10)

    def get_absolute_url(self):
        thread_url = reverse("punkweb_bb:thread", args=[self.thread.id])

        thread_url += f"?page={self.page_number}#post-{self.id}"

        return thread_url

    def save(self, *args, **kwargs):
        if self.thread.is_closed:
            raise ValidationError("Cannot add posts to a closed thread.")
        if self._state.adding:
            self.thread.last_post_created_at = timezone.now()
            self.thread.save()
        super().save(*args, **kwargs)


class Shout(UUIDPrimaryKeyMixin, TimestampMixin):
    user = models.ForeignKey(User, related_name="shouts", on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} > {self.created_at}"
