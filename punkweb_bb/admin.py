from django.contrib import admin
from django.utils.safestring import mark_safe

from .admin_forms import (
    BoardProfileAdminForm,
    CategoryAdminForm,
    PostAdminForm,
    SubcategoryAdminForm,
    ThreadAdminForm,
)
from .models import BoardProfile, Category, Post, Shout, Subcategory, Thread


@admin.register(BoardProfile)
class BoardProfileAdmin(admin.ModelAdmin):
    form = BoardProfileAdminForm
    list_display = [
        "user",
    ]
    list_filter = [
        "created_at",
        "user__is_active",
        "user__is_staff",
        "user__is_superuser",
    ]
    search_fields = [
        "user__username",
        "user__email",
    ]
    readonly_fields = [
        "signature_rendered",
    ]

    def signature_rendered(self, obj):
        return mark_safe(obj.signature.rendered)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = [
        "name",
        "order",
    ]
    search_fields = [
        "name",
        "description",
    ]
    prepopulated_fields = {
        "slug": [
            "name",
        ]
    }


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    form = SubcategoryAdminForm
    list_display = [
        "name",
        "category",
        "order",
    ]
    list_filter = [
        "category",
    ]
    search_fields = [
        "name",
        "description",
    ]
    prepopulated_fields = {
        "slug": [
            "name",
        ]
    }


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    form = ThreadAdminForm
    list_display = [
        "title",
        "subcategory",
        "user",
        "created_at",
    ]
    list_filter = [
        "subcategory",
        "created_at",
    ]
    search_fields = [
        "user__username",
        "user__email",
        "title",
        "content",
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        "thread",
        "user",
        "created_at",
    ]
    search_fields = [
        "user__username",
        "user__email",
        "content",
    ]


@admin.register(Shout)
class ShoutAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "created_at",
    ]
    search_fields = [
        "user__username",
        "user__email",
        "content",
    ]
