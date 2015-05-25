from lxml import etree
from defusedxml import lxml


class XMLObject(object):

    def __getattr__(self, item):
        return self.element.find('{attr}'.format(attr=item)).text


class Feed(XMLObject):

    def __init__(self, raw=None):
        if raw:
            self.element = lxml.fromstring(raw).find('channel')
        else:
            self.element = etree.Element('channel')

    def __iter__(self):
        for post_element in self.element.findall('item'):
            yield Post(element=post_element)

    @property
    def raw(self):
        return etree.tostring(self.element.getroottree())


class Post(XMLObject):

    def __init__(self, element=None):
        self.element = element
