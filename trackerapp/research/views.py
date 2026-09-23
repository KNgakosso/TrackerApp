from functools import wraps

from django.conf import settings
from django.shortcuts import render

from ..research.api.tenrai import tenrai_services
from .forms import SearchForm

# Create your views here.


def handle_api_errors(view):

    @wraps(view)
    def wrapper(request, *args, **kwargs):

        try:
            return view(request, *args, **kwargs)

        except ExternalApiError:

            return render(
                request,
                "tracking/api_error.html",
                status=503,
            )

    return wrapper


@handle_api_errors
def research(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_results = tenrai_services.research_media(search_form)
            return render(
                request,
                "tracking/research.html",
                context={
                    "search_results": search_results,
                    "search_form": search_form,
                    "settings_SFW": settings.SFW,
                },
            )
    else:
        search_form = SearchForm()
    return render(
        request,
        "tracking/research.html",
        context={
            "search_form": search_form,
            "settings_SFW": settings.SFW,
        },
    )
