import datetime

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from punkweb_bb.pagination import paginate_qs

from punkweb_bb.forms import (
    BoardAuthenticationForm,
    BoardProfileModelForm,
    BoardRegistrationForm,
    PostModelForm,
    ShoutModelForm,
    ThreadModelForm,
)
from punkweb_bb.models import Category, Post, Shout, Subcategory, Thread
from punkweb_bb.response import htmx_redirect

User = get_user_model()


def index(request):
    categories = Category.objects.all()

    recent_threads = Thread.objects.all().order_by("-created_at")[:5]

    thread_count = Thread.objects.count()
    post_count = Post.objects.count()

    users = User.objects.select_related("profile").all()
    newest_user = users.order_by("-profile__created_at").first()
    users_online = [user for user in users if user.profile.is_online]

    context = {
        "categories": categories,
        "recent_threads": recent_threads,
        "thread_count": thread_count,
        "post_count": post_count,
        "users": users,
        "newest_user": newest_user,
        "users_online": users_online,
    }
    return render(request, "punkweb_bb/index.html", context=context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("punkweb_bb:index")

    if request.method == "POST":
        form = BoardAuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("punkweb_bb:index")
    else:
        form = BoardAuthenticationForm()

    context = {
        "form": form,
    }
    return render(request, "punkweb_bb/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("punkweb_bb:login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("punkweb_bb:index")

    if request.method == "POST":
        form = BoardRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("punkweb_bb:login")
    else:
        form = BoardRegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "punkweb_bb/register.html", context)


@login_required(login_url="/login/")
def profile_detail(request):
    return render(request, "punkweb_bb/profile_detail.html")


@login_required(login_url="/login/")
def profile_update(request):
    if request.method == "POST":
        form = BoardProfileModelForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if form.is_valid():
            form.save()

            return redirect("punkweb_bb:profile_update")

    form = BoardProfileModelForm(instance=request.user.profile)

    context = {
        "form": form,
    }

    return render(request, "punkweb_bb/profile_update.html", context=context)


def subcategory_detail(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    threads = paginate_qs(request, subcategory.threads.all())

    context = {
        "subcategory": subcategory,
        "threads": threads,
    }
    return render(request, "punkweb_bb/subcategory_detail.html", context=context)


@login_required(login_url="/login/")
def thread_create(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    if request.method == "POST":
        form = ThreadModelForm(request.POST)

        if form.is_valid():
            thread = form.save(commit=False)
            thread.subcategory = subcategory
            thread.user = request.user
            thread.save()

            return redirect(thread)
    else:
        form = ThreadModelForm()

    context = {
        "subcategory": subcategory,
        "form": form,
    }
    return render(request, "punkweb_bb/thread_create.html", context=context)


def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    posts = paginate_qs(request, thread.posts.all())

    post_form = PostModelForm()

    context = {
        "thread": thread,
        "posts": posts,
        "post_form": post_form,
    }
    return render(request, "punkweb_bb/thread_detail.html", context=context)


@login_required(login_url="/login/")
def thread_update(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id, user=request.user)

    if request.method == "POST":
        form = ThreadModelForm(request.POST, instance=thread)

        if form.is_valid():
            thread = form.save()

            return redirect(thread)
    else:
        form = ThreadModelForm(instance=thread)

    context = {
        "thread": thread,
        "form": form,
    }
    return render(request, "punkweb_bb/thread_update.html", context=context)


@login_required(login_url="/login/")
def thread_delete(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id, user=request.user)

    if request.method == "DELETE":
        thread.delete()

        return htmx_redirect(thread.subcategory.get_absolute_url())

    context = {
        "thread": thread,
    }

    return render(request, "punkweb_bb/partials/thread_delete.html", context=context)


@login_required(login_url="/login/")
def post_create(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    form = PostModelForm(request.POST)

    if form.is_valid():
        post = form.save(commit=False)
        post.thread = thread
        post.user = request.user
        post.save()

        return redirect(post)


@login_required(login_url="/login/")
def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)

    if request.method == "POST":
        form = PostModelForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save()

            return redirect(post)

    form = PostModelForm(instance=post)

    context = {
        "post": post,
        "form": form,
    }

    return render(request, "punkweb_bb/partials/post_update.html", context=context)


@login_required(login_url="/login/")
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)

    if request.method == "DELETE":
        post.delete()

        return htmx_redirect(post.thread.get_absolute_url())

    context = {
        "post": post,
    }

    return render(request, "punkweb_bb/partials/post_delete.html", context=context)


def current_shouts():
    return Shout.objects.filter(
        created_at__gt=timezone.now() - datetime.timedelta(hours=12)
    ).order_by("created_at")


def shout_list(request):
    shouts = current_shouts()

    context = {
        "shouts": shouts,
    }
    return render(request, "punkweb_bb/shoutbox/shout_list.html", context=context)


def shout_create(request):
    if not request.user.is_authenticated:
        context = {
            "shouts": current_shouts(),
        }
        return render(request, "punkweb_bb/shoutbox/shout_list.html", context=context)

    if request.method == "POST":
        form = ShoutModelForm(request.POST)

        if form.is_valid():
            shout = form.save(commit=False)
            shout.user = request.user
            shout.save()

            context = {
                "shouts": current_shouts(),
            }
            return render(
                request, "punkweb_bb/shoutbox/shout_list.html", context=context
            )
