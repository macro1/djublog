import os

from django.conf import settings
from django.test import TestCase
import responses

from djublog import models


class TestFollowedFeed(TestCase):

    def setUp(self):
        self.followed = models.Followed.objects.create(url='http://microblog.brianschrader.com/feed')
        with open(os.path.join(settings.BASE_DIR, 'tests', 'fixtures', 'sonic_feed.xml')) as fixture_file:
            self.test_feed = fixture_file.read()
        responses.add(responses.GET, self.followed.url, body=self.test_feed,
                      status=200, content_type='application/xml')
        self.maxDiff = None

    @responses.activate
    def test_raw_feed(self):
        self.assertEqual(self.followed.feed.raw, self.test_feed)

    @responses.activate
    def test_user_info(self):
        self.assertEqual(self.followed.feed.username, 'sonicrocketman')
        self.assertEqual(self.followed.feed.user_id, '1234567890')
        self.assertEqual(self.followed.feed.user_full_name, 'Brian Schrader')
