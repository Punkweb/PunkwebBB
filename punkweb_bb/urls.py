from django.urls import path

from punkweb_bb import views

app_name = "punkweb_bb"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("settings/", views.settings_view, name="settings"),
    path("members/", views.members_view, name="members"),
    path("members/<path:user_id>/", views.profile_view, name="profile"),
    path(
        "subcategory/<str:subcategory_slug>/",
        views.subcategory_view,
        name="subcategory",
    ),
    path(
        "subcategory/<str:subcategory_slug>/create-thread/",
        views.thread_create_view,
        name="thread_create",
    ),
    path("thread/<str:thread_id>/", views.thread_view, name="thread"),
    path(
        "thread/<str:thread_id>/delete/", views.thread_delete_view, name="thread_delete"
    ),
    path(
        "thread/<str:thread_id>/update/", views.thread_update_view, name="thread_update"
    ),
    path(
        "thread/<str:thread_id>/create-post/",
        views.post_create_view,
        name="post_create",
    ),
    path("post/<str:post_id>/delete/", views.post_delete_view, name="post_delete"),
    path("post/<str:post_id>/update/", views.post_update_view, name="post_update"),
    path("shout-list/", views.shout_list_view, name="shout_list"),
    path("shout-create/", views.shout_create_view, name="shout_create"),
    path("bbcode/", views.bbcode_view, name="bbcode"),
]
