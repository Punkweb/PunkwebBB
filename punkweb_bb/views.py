import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, ShoutForm, ThreadForm
from .models import BoardProfile, Category, Shout, Subcategory, Post, Thread


def index(request):
    categories = Category.objects.all()

    recent_threads = Thread.objects.all().order_by("-created_at")[:5]
    recent_posts = Post.objects.all().order_by("-created_at")[:5]

    thread_count = Thread.objects.count()
    post_count = Post.objects.count()
    profile_count = BoardProfile.objects.count()
    newest_profile = BoardProfile.objects.order_by("-created_at").first()

    context = {
        "categories": categories,
        "recent_threads": recent_threads,
        "recent_posts": recent_posts,
        "thread_count": thread_count,
        "post_count": post_count,
        "profile_count": profile_count,
        "newest_profile": newest_profile,
    }
    return render(request, "punkweb_bb/index.html", context=context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("punkweb_bb:index")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("punkweb_bb:index")
    else:
        form = AuthenticationForm()

    context = {
        "form": form,
    }
    return render(request, "punkweb_bb/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("punkweb_bb:login")


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    context = {
        "category": category,
    }
    return render(request, "punkweb_bb/category_detail.html", context=context)


def subcategory_detail(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    context = {
        "subcategory": subcategory,
    }
    return render(request, "punkweb_bb/subcategory_detail.html", context=context)


@login_required(login_url="/login/")
def thread_create(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    if request.method == "POST":
        form = ThreadForm(request.POST)

        if form.is_valid():
            thread = form.save(commit=False)
            thread.subcategory = subcategory
            thread.user = request.user
            thread.save()

            return redirect("punkweb_bb:thread_detail", thread_id=thread.id)
    else:
        form = ThreadForm()

    context = {
        "subcategory": subcategory,
        "form": form,
    }
    return render(request, "punkweb_bb/thread_create.html", context=context)


def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    post_form = PostForm()

    context = {
        "thread": thread,
        "post_form": post_form,
    }
    return render(request, "punkweb_bb/thread_detail.html", context=context)


@login_required(login_url="/login/")
def post_create(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    form = PostForm(request.POST)

    if form.is_valid():
        post = form.save(commit=False)
        post.thread = thread
        post.user = request.user
        post.save()

        return redirect("punkweb_bb:thread_detail", thread_id=thread.id)


def current_shouts():
    return Shout.objects.filter(
        created_at__gt=datetime.datetime.today() - datetime.timedelta(hours=24)
    ).order_by("created_at")[:100]


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
        form = ShoutForm(request.POST)

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
