import os

from defusedxml import lxml
from django.conf import settings
from django.test import TestCase
import responses

from djublog import models


class TestFollowedFeed(TestCase):

    def setUp(self):
        self.followed = models.RemoteFeed.objects.create(feed_url='http://microblog.brianschrader.com/feed')
        with open(os.path.join(settings.BASE_DIR, 'tests', 'fixtures', 'sonic_feed.xml')) as fixture_file:
            self.test_feed = fixture_file.read()
        responses.add(responses.GET, self.followed.feed_url, body=self.test_feed,
                      status=200, content_type='application/xml')
        self.followed.update_feed()
        self.maxDiff = None

    @responses.activate
    def test_raw_feed(self):
        """Check that the raw feed is the full XML document"""
        self.assertEqual(self.followed.feed.raw[:5].decode('utf-8'), '<rss ')

    @responses.activate
    def test_user_info(self):
        self.assertEqual(self.followed.feed.username, 'sonicrocketman')
        self.assertEqual(self.followed.feed.user_id, '1234567890')
        self.assertEqual(self.followed.feed.user_full_name, 'Brian Schrader')
