from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from punkweb_bb.decorators import redirect_if_authenticated
from punkweb_bb.forms import (
    BoardProfileModelForm,
    CategoryModelForm,
    FilterUsersForm,
    LoginForm,
    PostModelForm,
    ShoutModelForm,
    SignUpForm,
    SubcategoryModelForm,
    ThreadModelForm,
    ThreadMoveForm,
)
from punkweb_bb.guests import guest_list
from punkweb_bb.models import Category, Post, Shout, Subcategory, Thread
from punkweb_bb.pagination import paginate
from punkweb_bb.response import htmx_redirect
from punkweb_bb.searching import search_threads
from punkweb_bb.utils import get_unique_slug

User = get_user_model()


def check_object_permission(obj, func, user):
    if not getattr(obj, func)(user):
        raise PermissionDenied


@redirect_if_authenticated()
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("punkweb_bb:login")
    else:
        form = SignUpForm()

    context = {
        "form": form,
    }
    return render(request, "punkweb_bb/signup.html", context)


@redirect_if_authenticated()
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("punkweb_bb:index")
    else:
        form = LoginForm()

    context = {
        "form": form,
    }
    return render(request, "punkweb_bb/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("punkweb_bb:login")


def index_view(request):
    categories = Category.objects.all()

    recent_threads = Thread.objects.all().order_by("-created_at")[:5]

    thread_count = Thread.objects.count()
    post_count = Post.objects.count()

    users = User.objects.select_related("profile").all()
    newest_user = users.order_by("-profile__created_at").first()

    users_online = [user for user in users if user.profile.is_online]
    members_online = [user for user in users_online if not user.is_staff]
    staff_online = [user for user in users_online if user.is_staff]
    guests_online = guest_list.length()
    total_online = len(members_online) + len(staff_online) + guests_online

    context = {
        "categories": categories,
        "recent_threads": recent_threads,
        "thread_count": thread_count,
        "post_count": post_count,
        "users": users,
        "newest_user": newest_user,
        "members_online": members_online,
        "staff_online": staff_online,
        "guests_online": guests_online,
        "total_online": total_online,
    }
    return render(request, "punkweb_bb/index.html", context=context)


def profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Get top threads by post count
    top_threads = user.threads.annotate(count_posts=Count("posts")).order_by(
        "-count_posts"
    )[:5]

    # Get top subcategories by thread count
    top_subcategories = (
        user.threads.values("subcategory")
        .annotate(count_threads=Count("subcategory"))
        .order_by("-count_threads")
    )
    for subcategory in top_subcategories:
        subcategory["subcategory"] = Subcategory.objects.get(
            pk=subcategory["subcategory"]
        )

    threads_qs = user.threads.all().order_by("-created_at")
    posts_qs = user.posts.all().order_by("-created_at")

    threads = paginate(request, threads_qs)
    posts = paginate(request, posts_qs)

    context = {
        "user": user,
        "top_threads": top_threads,
        "top_subcategories": top_subcategories,
        "threads": threads,
        "posts": posts,
    }

    return render(request, "punkweb_bb/profile.html", context=context)


def members_view(request):
    users_qs = User.objects.all()

    form = FilterUsersForm(request.GET)
    if form.is_valid():
        search = form.cleaned_data["search"]
        sort_by = form.cleaned_data["sort_by"]
        if search:
            users_qs = users_qs.filter(username__icontains=search)
        if sort_by:
            users_qs = users_qs.order_by(sort_by)
        else:
            users_qs = users_qs.order_by("username")

        users_qs = users_qs.select_related("profile")

    users = paginate(request, users_qs)

    context = {
        "form": form,
        "users": users,
    }
    return render(request, "punkweb_bb/members.html", context=context)


@login_required(login_url="/login/")
def settings_view(request):
    if request.method == "POST":
        form = BoardProfileModelForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if form.is_valid():
            form.save()

            return redirect("punkweb_bb:settings")
        else:
            return render(request, "punkweb_bb/settings.html", context={"form": form})

    form = BoardProfileModelForm(instance=request.user.profile)

    context = {
        "form": form,
    }

    return render(request, "punkweb_bb/settings.html", context=context)


@login_required(login_url="/login/")
@permission_required("punkweb_bb.view_category", raise_exception=True)
def category_create_view(request):
    if request.method == "POST":
        form = CategoryModelForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.slug = get_unique_slug(Category, category.name)
            category.save()

            return redirect(category)
    else:
        form = CategoryModelForm()

    context = {
        "form": form,
    }
    return render(request, "punkweb_bb/category_create.html", context=context)


@login_required(login_url="/login/")
@permission_required("punkweb_bb.change_category", raise_exception=True)
def category_update_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if request.method == "POST":
        form = CategoryModelForm(request.POST, instance=category)

        if form.is_valid():
            category = form.save()

            return redirect(category)
    else:
        form = CategoryModelForm(instance=category)

    context = {
        "category": category,
        "form": form,
    }
    return render(request, "punkweb_bb/category_update.html", context=context)


@login_required(login_url="/login/")
@permission_required("punkweb_bb.delete_category", raise_exception=True)
def category_delete_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if request.method == "DELETE":
        category.delete()

        return htmx_redirect(reverse("punkweb_bb:index"))

    context = {
        "category": category,
    }

    return render(request, "punkweb_bb/partials/category_delete.html", context=context)


def subcategory_view(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    threads = paginate(request, subcategory.threads.all())

    context = {
        "subcategory": subcategory,
        "threads": threads,
    }
    return render(request, "punkweb_bb/subcategory.html", context=context)


@login_required(login_url="/login/")
@permission_required("punkweb_bb.add_subcategory", raise_exception=True)
def subcategory_create_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if request.method == "POST":
        form = SubcategoryModelForm(request.POST)

        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.category = category
            subcategory.slug = get_unique_slug(Subcategory, subcategory.name)
            subcategory.save()

            return redirect(subcategory)
    else:
        form = SubcategoryModelForm(initial={"category": category})

    context = {
        "category": category,
        "form": form,
    }
    return render(request, "punkweb_bb/subcategory_create.html", context=context)


@login_required(login_url="/login/")
@permission_required("punkweb_bb.change_subcategory", raise_exception=True)
def subcategory_update_view(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    if request.method == "POST":
        form = SubcategoryModelForm(request.POST, instance=subcategory)

        if form.is_valid():
            subcategory = form.save()

            return redirect(subcategory)
    else:
        form = SubcategoryModelForm(instance=subcategory)

    context = {
        "subcategory": subcategory,
        "form": form,
    }
    return render(request, "punkweb_bb/subcategory_update.html", context=context)


@login_required(login_url="/login/")
@permission_required("punkweb_bb.delete_subcategory", raise_exception=True)
def subcategory_delete_view(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    if request.method == "DELETE":
        subcategory.delete()

        return htmx_redirect(subcategory.category.get_absolute_url())

    context = {
        "subcategory": subcategory,
    }

    return render(
        request, "punkweb_bb/partials/subcategory_delete.html", context=context
    )


@login_required(login_url="/login/")
def thread_create_view(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    check_object_permission(subcategory, "can_post", request.user)

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


def thread_view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    posts = paginate(request, thread.posts.all())

    post_form = PostModelForm()

    # Increment view count if this session hasn't viewed the thread before
    viewed_threads = request.session.get("viewed_threads", [])
    if thread_id not in viewed_threads:
        thread.view_count += 1
        thread.save()
        request.session["viewed_threads"] = viewed_threads + [thread_id]

    context = {
        "thread": thread,
        "posts": posts,
        "post_form": post_form,
    }
    return render(request, "punkweb_bb/thread.html", context=context)


@login_required(login_url="/login/")
def thread_update_view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    check_object_permission(thread, "can_edit", request.user)

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
def thread_delete_view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    check_object_permission(thread, "can_delete", request.user)

    if request.method == "DELETE":
        thread.delete()

        return htmx_redirect(thread.subcategory.get_absolute_url())

    context = {
        "thread": thread,
    }

    return render(request, "punkweb_bb/partials/thread_delete.html", context=context)


@login_required(login_url="/login/")
@permission_required("punkweb_bb.pin_thread", raise_exception=True)
def thread_pin_view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    thread.is_pinned = not thread.is_pinned
    thread.save()

    return htmx_redirect(thread.get_absolute_url())


@login_required(login_url="/login/")
@permission_required("punkweb_bb.close_thread", raise_exception=True)
def thread_close_view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    thread.is_closed = not thread.is_closed
    thread.save()

    return htmx_redirect(thread.get_absolute_url())


@login_required(login_url="/login/")
@permission_required("punkweb_bb.move_thread", raise_exception=True)
def thread_move_view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.method == "POST":
        form = ThreadMoveForm(request.POST)

        if form.is_valid():
            thread.subcategory = form.cleaned_data["subcategory"]
            thread.save()

            return redirect(thread)

    initial_data = {
        "subcategory": thread.subcategory,
    }

    form = ThreadMoveForm(data=initial_data)

    context = {
        "thread": thread,
        "form": form,
    }

    return render(request, "punkweb_bb/partials/thread_move.html", context=context)


@login_required(login_url="/login/")
def post_create_view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    check_object_permission(thread, "can_post", request.user)

    form = PostModelForm(request.POST)

    if form.is_valid():
        post = form.save(commit=False)
        post.thread = thread
        post.user = request.user
        post.save()

        return redirect(post)


@login_required(login_url="/login/")
def post_update_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    check_object_permission(post, "can_edit", request.user)

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
def post_delete_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    check_object_permission(post, "can_delete", request.user)

    if request.method == "DELETE":
        post.delete()

        return htmx_redirect(post.thread.get_absolute_url())

    context = {
        "post": post,
    }

    return render(request, "punkweb_bb/partials/post_delete.html", context=context)


def current_shouts():
    return Shout.objects.filter(
        created_at__gt=timezone.now() - timezone.timedelta(hours=12)
    ).order_by("created_at")


def shout_list_view(request):
    shouts = current_shouts()

    context = {
        "shouts": shouts,
    }
    return render(request, "punkweb_bb/shoutbox/shout_list.html", context=context)


def shout_create_view(request):
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


@login_required(login_url="/login/")
def shout_delete_view(request, shout_id):
    shout = get_object_or_404(Shout, pk=shout_id)

    check_object_permission(shout, "can_delete", request.user)

    if request.method == "DELETE":
        shout.delete()

        return htmx_redirect(reverse("punkweb_bb:index"))

    context = {
        "shout": shout,
    }

    return render(request, "punkweb_bb/partials/shout_delete.html", context=context)


def bbcode_view(request):
    codes = (
        ("Bold", "[b]Bold Text[/b]"),
        ("Italic", "[i]Italic Text[/i]"),
        ("Underline", "[u]Underlined Text[/u]"),
        ("Strikethrough", "[s]Strikethrough Text[/s]"),
        ("Color", "[color=red]Red Text[/color]"),
        ("Font", "[font=serif]Serif Text[/font]"),
        ("Shadow", "[shadow=red]Red Shadow Text[/shadow]"),
        ("Size", "[size=7]Size 7 Text[/size]"),
        ("Superscript", "Sup [sup]Superscript Text[/sup]"),
        ("Subscript", "Sub [sub]Subscript Text[/sub]"),
        ("Horizontal Rule", "[hr]"),
        ("Left", "[left]Left Text[/left]"),
        ("Center", "[center]Centered Text[/center]"),
        ("Right", "[right]Right Text[/right]"),
        ("Quote", "[quote=Example]Quoted Text[/quote]"),
        ("Url", "[url=https://google.com]Link Text[/url]"),
        (
            "Image",
            "[img]https://placehold.co/400[/img]",
        ),
        (
            "Code",
            """
[code=python]
class ThreadModelForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = (
            "title",
            "content",
        )
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": True, "class": "pw-input"}),
            "content": BBCodeEditorWidget(),
        }
[/code]
""",
        ),
        ("Ordered List", "[ol][li]Item 1[/li][li]Item 2[/li][/ol]"),
        ("Unordered List", "[ul][li]Item 1[/li][li]Item 2[/li][/ul]"),
        ("Escape", "[escape][b]Escaped bbcode[/b][/escape]"),
    )

    context = {
        "codes": codes,
    }

    return render(request, "punkweb_bb/bbcode.html", context=context)


def search_view(request):
    query = request.GET.get("q", "")

    print(query)

    matching_threads = search_threads(query)

    print(matching_threads)

    context = {
        "query": query,
        "threads": matching_threads,
    }

    return render(request, "punkweb_bb/search.html", context=context)
