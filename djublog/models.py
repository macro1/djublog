from defusedxml import lxml
from django.db import models
import requests


class Feed(object):

    def __init__(self, raw=None):
        self.raw = raw
        self.tree = lxml.fromstring(raw).getroottree()

    @property
    def username(self):
        return self.tree.find('/channel/username').text

    @property
    def user_id(self):
        return self.tree.find('/channel/user_id').text

    @property
    def user_full_name(self):
        return self.tree.find('/channel/user_full_name').text


class Followed(models.Model):
    url = models.URLField()

    @property
    def feed(self):
        return Feed(requests.get(self.url).text)
