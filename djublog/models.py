import logging

from django.conf import settings
from django.db import models
from django.utils import timezone
import requests

from . import feed

logger = logging.getLogger()


class Feed(models.Model):
    FIELDS = (
        ('username', 'username'),
        ('userid', 'user_id'),
        ('profile_url', 'profile'),
        ('feed_url', 'link'),
        ('language', 'language'),
        ('build_date', 'lastBuildDate'),
    )

    username = models.CharField(editable=False, max_length=100, null=True)
    userid = models.CharField(editable=False, max_length=100, null=True)
    profile_url = models.URLField(editable=False, null=True)
    language = models.CharField(editable=False, max_length=100, null=True)
    build_date = models.DateTimeField(editable=False, null=True)
    raw_feed = models.TextField(editable=False, null=True)

    def __str__(self):
        return '{}: {}'.format(self._meta.verbose_name, self.username)


class LocalFeed(Feed):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    @property
    def feed(self):
        return feed.Feed(self.raw_feed)


class RemoteFeed(Feed):
    feed_url = models.URLField()

    @property
    def feed(self):
        return feed.Feed(self.raw_feed)

    def update_feed(self):
        self.raw_feed = requests.get(self.feed_url).text
        feed = self.feed
        for dest, source in self.FIELDS:
            try:
                value = getattr(feed, source)
            except Exception as e:
                logger.exception(e)
            else:
                setattr(self, dest, value)
        for post in feed:
            self.post_set.update_or_create(
                statusid=post.guid,
                defaults={
                    'description': post.description,
                },
            )
        self.build_date = self.build_date or timezone.now()



class Post(models.Model):
    FIELDS = (
        ('statusid', 'status_id'),
        ('description', 'description'),
    )
    feed = models.ForeignKey(Feed)
    statusid = models.CharField(max_length=100, editable=False)
    description = models.TextField()

    class Meta:
        unique_together = (
            ('feed', 'statusid'),
        )

    def save(self, *args, **kwargs):
        if not self.statusid and not self.pk:
            self.statusid = models.F('pk')
        super(Post, self).save(*args, **kwargs)
