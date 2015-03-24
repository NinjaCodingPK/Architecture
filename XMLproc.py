from lxml import etree
from lxml import html
import urllib
# from lxml.builder import E

# -*- coding: utf-8 -*-


class Xmlproc:

    root = []
    tree = []
    arr = []

    def __init__(self):
        self.root = etree.Element("root")

    def add(self, elem, time):
        if (self.notsameadd(elem) == 1):
            return 1

        field1 = etree.SubElement(self.root, "film")

        field2 = etree.SubElement(field1, "name")
        field2.text = elem

        field2 = etree.SubElement(field1, "time")
        field2.text = time

    def notsameadd(self, elem):
        for i in self.arr:
            if i == elem:
                return 1

        self.arr.append(elem)
        return 0

    def writefile(self, filename):
        f = open(filename, 'w')

        f.write(etree.tostring(self.root, pretty_print=True, encoding='utf8'))
        f.close()


class TakeXml:
    def __init__(self, filename):
        response = urllib.urlopen(filename)
        htmlpage = response.read()
        self.xmlf = html.document_fromstring(htmlpage)

    def get_href_buf(self):
        hrefs = self.xmlf.xpath("//a")
        return hrefs

    def get_time_buf(self):
        temp = self.xmlf.xpath("//time/text()")
        return temp

    def get_name_buf(self):
        temp = self.xmlf.xpath("//name/text()")
        return temp
