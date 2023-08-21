from django.urls import path

from . import views


app_name = "punkweb_bb"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "category/<str:category_slug>/", views.category_detail, name="category_detail"
    ),
    path(
        "subcategory/<str:subcategory_slug>/",
        views.subcategory_detail,
        name="subcategory_detail",
    ),
    path(
        "subcategory/<str:subcategory_slug>/create-thread/",
        views.thread_create,
        name="thread_create",
    ),
    path("thread/<str:thread_id>/", views.thread_detail, name="thread_detail"),
    path("thread/<str:thread_id>/create-post/", views.post_create, name="post_create"),
]
