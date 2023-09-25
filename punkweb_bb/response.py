from django.http import HttpResponse


def htmx_redirect(url):
    return HttpResponse(content=b"", headers={"HX-Redirect": url})
