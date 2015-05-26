from lxml import etree
from defusedxml import lxml


class XMLObject(object):
    RESERVED = ('element',)

    def __getattr__(self, name):
        return self.element.find(name).text

    def __setattr__(self, name, value):
        if name in self.RESERVED:
            return super(XMLObject, self).__setattr__(name, value)
        element = self.element.find(name)
        if not element:
            element = etree.SubElement(self.element, name)
        element.text = value


class Feed(XMLObject):

    def __init__(self, posts=None, raw=None):
        if raw:
            self.element = lxml.fromstring(raw).find('channel')
        else:
            root = etree.Element('rss', attrib={'extension': 'microblog', 'version': '2.0'})
            self.element = etree.SubElement(root, 'channel')
            for post in posts:
                self.element.append(post)

    def __iter__(self):
        for post_element in self.element.findall('item'):
            yield Post(element=post_element)

    @property
    def raw(self):
        return etree.tostring(self.element.getroottree(), pretty_print=True)


class Post(XMLObject):

    def __init__(self, element=None):
        if element:
            self.element = element
        else:
            self.element = etree.Element('item')
