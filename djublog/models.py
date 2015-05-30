import datetime
import email.utils
import uuid
import logging

from django.conf import settings
from django.core import urlresolvers
from django.db import models
from django.utils import timezone
import requests

from . import feed

logger = logging.getLogger()


class BaseFeed(models.Model):
    FIELDS = (
        ('username', 'username'),
        ('userid', 'user_id'),
        ('profile_url', 'profile'),
        ('feed_url', 'link'),
        ('language', 'language'),
        ('build_date', 'lastBuildDate'),
    )
    language = models.CharField(editable=False, max_length=100, null=True)


class LocalFeed(BaseFeed):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, editable=False)

    def __str__(self):
        return '{}: {}'.format(self._meta.verbose_name, self.username)

    @property
    def feed(self):
        post_elements = []
        for post in self.post_set.all():
            post_element = feed.Post()
            post_element.status_id = post.statusid
            post_element.description = post.description
            post_elements.append(post_element.element)
        new_feed = feed.Feed(post_elements)
        new_feed.username = self.user.username
        new_feed.user_id = str(self.user.pk)
        try:
            new_feed.profile = urlresolvers.reverse('ufeed', kwargs={'username': self.user.username})
        except urlresolvers.NoReverseMatch:
            new_feed.profile = urlresolvers.reverse('ufeed')
        try:
            new_feed.link = urlresolvers.reverse('ufeed', kwargs={'username': self.user.username})
        except urlresolvers.NoReverseMatch:
            new_feed.link = urlresolvers.reverse('ufeed')
        new_feed.language = self.language
        epoch = timezone.make_aware(datetime.datetime.utcfromtimestamp(0), timezone.utc)
        epoch_time = (timezone.now() - epoch).total_seconds()
        new_feed.lastBuildDate = email.utils.formatdate(epoch_time)
        return new_feed

    @property
    def username(self):
        return self.user.username

    @property
    def raw_feed(self):
        return self.feed.raw


class RemoteFeed(BaseFeed):
    feed_url = models.URLField()
    username = models.CharField(editable=False, max_length=100, null=True)
    userid = models.CharField(editable=False, max_length=100, null=True)
    profile_url = models.URLField(editable=False, null=True)
    build_date = models.DateTimeField(editable=False, null=True)
    raw_feed = models.TextField(editable=False, null=True)

    def __str__(self):
        return '{}: {}'.format(self._meta.verbose_name, self.username)

    @property
    def feed(self):
        return feed.Feed(raw=self.raw_feed)

    def update_feed(self):
        self.raw_feed = requests.get(
            self.feed_url,
            headers={'content-type': 'application/rss+xml'},
        ).text
        feed = self.feed
        for dest, source in self.FIELDS:
            try:
                value = getattr(feed, source)
            except Exception as e:
                logger.exception(e)
            else:
                setattr(self, dest, value)
        self.save()
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
    feed = models.ForeignKey(BaseFeed)
    statusid = models.CharField(max_length=100, editable=False)
    description = models.TextField()

    class Meta:
        unique_together = (
            ('feed', 'statusid'),
        )

    def save(self, *args, **kwargs):
        set_id = False
        if not self.statusid and not self.pk:
            self.statusid = uuid.uuid4().hex
        super(Post, self).save(*args, **kwargs)
        if set_id:
            self.statusid = self.pk
            self.save()
