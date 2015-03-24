import unittest
import XMLproc
import htmlparser
from lxml import html

# -*- coding: utf-8 -*-


class TestXml(unittest.TestCase):
    def test_add(self):
        fileout = XMLproc.Xmlproc()
        self.assertNotEqual(fileout.add("Name", "1:50"), 1)

    def testnotsameadd(self):
        fileout = XMLproc.Xmlproc()
        fileout.add("Name", "00:30")
        self.assertEqual(fileout.notsameadd("Name"), 1)

    def testgettime(self):
        testparser = htmlparser.HtmlParser()
        self.assertEqual(testparser.gettime("aa"), 'Error')

    def testgetnoneinfo(self):
        tempstr = """<html>
                    <h1>Name</h1>
                    <h2>2:00</h2>
                </html>"""
        current_page = html.document_fromstring(tempstr)
        testparser = htmlparser.HtmlParser()
        name = current_page.xpath('//h1')
        time = current_page.xpath('//h2')
        self.assertEqual(testparser.getinfo(name, time, 0, testparser.constnames), None)

    def testgetinfo(self):
        tempstr = """<html>
                    <h1>Name</h1>
                    <h2>0:10</h2>
                    <h1>Film</h1>
                    <h2>0:20</h2>
                </html>"""
        buf = (u'Name', u'0:10:00')
        const = ['Name', 'Film']
        current_page = html.document_fromstring(tempstr.decode('utf8'))
        testparser = htmlparser.HtmlParser()
        name = current_page.xpath('//h1')
        time = current_page.xpath('//h2')
        self.assertEqual(testparser.getinfo(name, time, 0, const), buf)

    def testget_href(self):
        tempxml = XMLproc.TakeXml("testin.xml")
        self.assertEqual(tempxml.get_href_buf()[0].get('href'), "http://1tv.com.ua/uk/tv/2015/02/27")

    def testget_name(self):
        tempxml = XMLproc.TakeXml("testin.xml")
        self.assertEqual(tempxml.get_name_buf()[0], "//div[@class='b-tvlist-title']/a | //div[@class='b-tvlist-title']")

    def testget_time(self):
        tempxml = XMLproc.TakeXml("testin.xml")
        self.assertEqual(tempxml.get_time_buf()[0], "//tr/td[1]")

    def test_parse(self):
        tempxml = XMLproc.TakeXml("in.xml")
        testparser = htmlparser.HtmlParser()
        href_buf = tempxml.get_href_buf()
        time_buf = tempxml.get_time_buf()
        name_buf = tempxml.get_name_buf()

        self.assertEqual(testparser.parse(href_buf[0], name_buf[0], time_buf[0]), True)

if __name__ == "__main__":
    unittest.main()
