import os

from django.conf import settings
from django.contrib import auth
from django.test import TestCase
import responses

from djublog import models


class TestBaseFeed(TestCase):

    def setUp(self):
        self.feed = models.BaseFeed.objects.create()

    def test_str(self):
        self.assertEqual(str(self.feed), 'BaseFeed object')


class TestLocalFeed(TestCase):

    def setUp(self):
        self.user = auth.get_user_model().objects.create(username='tester')
        self.feed = models.LocalFeed.objects.create(user=self.user)

    def test_str(self):
        self.assertEqual(str(self.feed), 'local feed: tester')


class TestRemoteFeed(TestCase):

    def setUp(self):
        feed_url = 'http://microblog.brianschrader.com/feed'
        self.feed = models.RemoteFeed.objects.create(feed_url=feed_url)
        with open(os.path.join(settings.BASE_DIR, 'tests', 'fixtures', 'sonic_feed.xml')) as fixture_file:
            self.test_feed = fixture_file.read()
        responses.add(responses.GET, feed_url, body=self.test_feed,
                      status=200, content_type='application/xml')
        responses.start()
        self.feed.update_feed()

    def tearDown(self):
        responses.stop()

    def test_str(self):
        self.assertEqual(str(self.feed), 'remote feed: sonicrocketman')

    def test_raw_feed(self):
        """Check that the raw feed is the full XML document"""
        self.assertEqual(self.feed.feed.raw[:6].decode('utf-8'), "<?xml ")

    def test_user_info(self):
        self.assertEqual(self.feed.feed.username, 'sonicrocketman')
        self.assertEqual(self.feed.feed.user_id, '1234567890')
        self.assertEqual(self.feed.feed.user_full_name, 'Brian Schrader')

    def test_save_feed(self):
        feed = models.RemoteFeed(feed_url='http://microblog.brianschrader.com/feed')
        feed.update_feed()


class TestPost(TestCase):

    def setUp(self):
        self.feed = models.BaseFeed.objects.create()

    def test_statusid_is_set(self):
        post = models.Post(feed=self.feed)
        self.assertFalse(post.statusid)
        post.save()
        self.assertIsNotNone(post.statusid)
