# -*- coding: utf-8 -*-
import urllib
# import urllib2
import datetime
# import time
from lxml import html
# from lxml import etree
import XMLproc


class HtmlParser:
    def __init__(self):
        self.outf = 'out.xml'
        self.inf = 'in.xml'
        self.constnames = [u'Серіал', u'Т/с']
        # self.fileout = XMLproc.Xmlproc()
        self.hour = 1
        self.minute = 45

# @staticmethod
# def urlopen(url):
# response = urllib.urlopen(url)
# htmlpage = response.read()
# return html.document_fromstring(htmlpage)

    @staticmethod
    def gettime(strtime):
        try:
            return datetime.datetime.strptime(strtime, '%H:%M')
        except ValueError:
            return 'Error'

    def getinfo(self, namesbuf, timesbuf, i, const):
        if (const[0] in unicode(namesbuf[i].text)) or \
                (const[1] in unicode(namesbuf[i].text)):
                deltatime = self.gettime(timesbuf[i + 1].text) - \
                    self.gettime(timesbuf[i].text)
                realminutes = (deltatime.seconds +
                               deltatime.microseconds/1000000.0)/60.0
                realtime = datetime.timedelta(days=0, minutes=realminutes)
                if realtime < datetime.timedelta(hours=self.hour, minutes=self.minute):
                    return unicode(namesbuf[i].text), unicode(realtime)
                    # self.fileout.add(unicode(namesbuf[i].text), unicode(realtime))
        return None

    def parse(self, urlpath, namepath, timepath):
        fileout = XMLproc.Xmlproc()

        response = urllib.urlopen(urlpath.get('href'))
        htmlpage = response.read()
        current_page = html.document_fromstring(htmlpage)

        times = current_page.xpath(timepath)
        names = current_page.xpath(namepath)

        i = 0
        while (i < len(times) - 1) and (i < len(names) - 1):
            buf = self.getinfo(names, times, i, self.constnames)
            if buf:
                fileout.add(buf[0], buf[1])
            i += 1

        fileout.writefile(self.outf)
        return True