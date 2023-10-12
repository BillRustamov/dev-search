from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger

from . import models


def search_profiles(request):
    profiles = models.Profile.objects.exclude(
        Q(short_intro=None) |
        Q(location=None) |
        Q(description=None) |
        Q(short_intro="") |
        Q(location="") |
        Q(description="")
    )

    q = request.GET.get('q')  # "Python" or None
    if q:
        # contains -> case sensitivity
        # icontains -> ignores case sensitivity
        profiles = profiles.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(location__icontains=q) |
            Q(short_intro__icontains=q) |
            Q(skill__name__icontains=q)
        ).distinct()

    return request, profiles


def paginate_profiles(request, profiles):
    paginator = Paginator(profiles, 6)

    # <Page 1 of 4>
    page = paginator.page(1)

    if request.GET.get('page'):
        # <page 1
        try:
            page = paginator.page(request.GET.get('page'))
        except (EmptyPage, PageNotAnInteger):
            page = paginator.page(1)

    start_index = page.number - 2
    if start_index <= 0:
        start_index = 1

    end_index = page.number + 2
    if end_index >= paginator.num_pages:
        end_index = paginator.num_pages

    return range(start_index, end_index + 1), page
