from django.contrib import admin
from django.utils.safestring import mark_safe

from punkweb_bb.admin_forms import (
    BoardProfileAdminModelForm,
    CategoryAdminModelForm,
    PostAdminModelForm,
    SubcategoryAdminModelForm,
    ThreadAdminModelForm,
)
from punkweb_bb.models import BoardProfile, Category, Post, Shout, Subcategory, Thread


@admin.register(BoardProfile)
class BoardProfileModelAdmin(admin.ModelAdmin):
    form = BoardProfileAdminModelForm
    list_display = ("user",)
    list_filter = (
        "created_at",
        "user__is_active",
        "user__is_staff",
        "user__is_superuser",
    )
    search_fields = (
        "user__username",
        "user__email",
    )
    readonly_fields = ("signature_rendered",)

    def signature_rendered(self, obj):
        return mark_safe(obj.signature.rendered)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    form = CategoryAdminModelForm
    list_display = (
        "name",
        "order",
    )
    search_fields = (
        "name",
        "description",
    )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Subcategory)
class SubcategoryModelAdmin(admin.ModelAdmin):
    form = SubcategoryAdminModelForm
    list_display = (
        "name",
        "category",
        "order",
    )
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Thread)
class ThreadModelAdmin(admin.ModelAdmin):
    form = ThreadAdminModelForm
    list_display = (
        "title",
        "subcategory",
        "user",
        "created_at",
        "last_post_created_at",
        "is_pinned",
        "is_closed",
    )
    list_filter = (
        "subcategory",
        "created_at",
        "last_post_created_at",
        "is_pinned",
        "is_closed",
    )
    search_fields = (
        "user__username",
        "user__email",
        "title",
        "content",
    )


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    form = PostAdminModelForm
    list_display = (
        "thread",
        "user",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__email",
        "content",
    )


@admin.register(Shout)
class ShoutModelAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__email",
        "content",
    )
