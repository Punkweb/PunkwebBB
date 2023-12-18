from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate_qs(request, qs, page_size=10):
    paginator = Paginator(qs, page_size)

    page = request.GET.get("page", 1)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return results
