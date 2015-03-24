import htmlparser
import time
import XMLproc
from ConfigParser import SafeConfigParser
import gevent
# from gevent import monkey

inf = 'in.xml'

testget = XMLproc.TakeXml(inf)
href_buf = testget.get_href_buf()
name_buf = testget.get_name_buf()
time_buf = testget.get_time_buf()

cfg = SafeConfigParser()
cfg.read('config.conf')
version = cfg.get('newconfiguration', 'launch')

if version == 'simple':
    start = time.time()

    newparser = htmlparser.HtmlParser()

    i = 0
    pathbuf = []
    for href in href_buf:
        newparser.parse(href, name_buf[i], time_buf[i])
        i += 1

    final = time.time()
    print "simple"
    print final - start


if version == 'mult':
    start = time.time()

    newparser = htmlparser.HtmlParser()

    i = 0

    threads = [gevent.spawn(newparser.parse, href_buf[i], name_buf[i], time_buf[i]) for i in range(len(href_buf))]
    # gevent.wait(threads)
    gevent.joinall(threads)

    final = time.time()
    print "mult"
    print final - start