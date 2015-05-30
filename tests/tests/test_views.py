from django import http
from django.contrib import auth
from django.test import TestCase

from djublog import models, views


class TestHTTPAccept(TestCase):

    def setUp(self):
        user = auth.get_user_model().objects.create(username='test_blogger')
        self.feed = models.LocalFeed.objects.create(user=user)

    def test_no_accept(self):
        request = http.HttpRequest()
        request.META.pop('HTTP_ACCEPT', None)
        response = views.feed_view(request)
        self.assertEqual(response.status_code, 200)
