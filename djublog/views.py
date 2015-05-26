from django import http
from django.shortcuts import get_object_or_404, render

from . import models


def feed_view(request, username=None):
    if username:
        feed = get_object_or_404(models.LocalFeed, username=username)
    else:
        try:
            feed = models.LocalFeed.objects.order_by('pk')[0]
        except IndexError:
            raise http.Http404('No {} matches the given query.'.format(models.LocalFeed._meta.object_name))
    context = {
        'feed': feed,
    }
    if 'text/html' in request.META.get('HTTP_ACCEPT') and request.GET.get('format') != 'rss':
        return render(request, content_type='text/html', context=context, template_name='djublog/feed.html')
    if 'application/rss+xml' in request.META.get('HTTP_ACCEPT'):
        content_type = 'application/rss+xml'
    else:
        content_type = 'application/xml'
    return http.HttpResponse(content=feed.raw_feed, content_type=content_type)
