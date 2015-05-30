from functools import partial

from lxml import etree
from defusedxml import lxml


class XMLObject(object):
    RESERVED = ('element',)
    UB_ELEMENTS = {'status_id', 'username', 'user_id', 'profile', 'link'}
    NSMAP = {
        'ub': 'https://github.com/Sonictherocketman/Open-Microblog',
    }

    def __getattr__(self, name):
        if name in self.UB_ELEMENTS:
            name = '{{{ns}}}{name}'.format(ns=self.NSMAP.get('ub'), name=name)
        return self.element.find(name).text

    def __setattr__(self, name, value):
        if name in self.RESERVED:
            return super(XMLObject, self).__setattr__(name, value)
        self.set_subelement(name, value)

    def set_subelement(self, name, value, ns=None):
        if name in self.UB_ELEMENTS:
            name = '{{{ns}}}{name}'.format(ns=self.NSMAP.get('ub'), name=name)
        element = self.element.find(name)
        if not element:
            element = etree.SubElement(self.element, name)
        element.text = value

class Feed(XMLObject):

    def __init__(self, posts=None, raw=None):
        if raw:
            self.element = lxml.fromstring(raw).find('channel')
        else:
            root = etree.Element('rss', attrib={'version': '2.0'}, nsmap=self.NSMAP)
            self.element = etree.SubElement(root, 'channel')
            for post in posts:
                self.element.append(post)

    def __iter__(self):
        for post_element in self.element.findall('item'):
            yield Post(element=post_element)

    username = property(fset=partial(XMLObject.set_subelement, ns='ublog'))

    @property
    def raw(self):
        return etree.tostring(self.element.getroottree(), encoding='utf-8', pretty_print=True, xml_declaration=True)


class Post(XMLObject):

    def __init__(self, element=None):
        if element:
            self.element = element
        else:
            self.element = etree.Element('item')
