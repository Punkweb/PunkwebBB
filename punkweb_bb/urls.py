from django.urls import path

from punkweb_bb import views

app_name = "punkweb_bb"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("members/", views.members, name="members"),
    path(
        "subcategory/<str:subcategory_slug>/",
        views.subcategory,
        name="subcategory",
    ),
    path(
        "subcategory/<str:subcategory_slug>/create-thread/",
        views.thread_create,
        name="thread_create",
    ),
    path("thread/<str:thread_id>/", views.thread, name="thread"),
    path("thread/<str:thread_id>/delete/", views.thread_delete, name="thread_delete"),
    path("thread/<str:thread_id>/update/", views.thread_update, name="thread_update"),
    path("thread/<str:thread_id>/create-post/", views.post_create, name="post_create"),
    path("post/<str:post_id>/delete/", views.post_delete, name="post_delete"),
    path("post/<str:post_id>/update/", views.post_update, name="post_update"),
    path("shout-list/", views.shout_list, name="shout_list"),
    path("shout-create/", views.shout_create, name="shout_create"),
    path("bbcode/", views.bbcode, name="bbcode"),
]
