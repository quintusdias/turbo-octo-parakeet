import re
import urllib

from lxml import etree
import requests

class WeatherDotGov(object):

    def __init__(self):

        self.wfo_regex = re.compile('^/(?P<wfo>[a-z]{3})/$')
        self.r = requests.get('http://www.weather.gov')
        self.wdg_doc = etree.HTML(self.r.content.decode('utf-8'))

    def run(self):
        areas = self.wdg_doc.xpath('//area')
        hrefs = set([elt.attrib['href'] for elt in areas])
        for area, href in zip(areas, hrefs):
            self.process_path(href)

    def process_path(self, href):
        """
        Parameters
        ----------
        href : str
            URL from weather.gov homepage
        """
        o = urllib.parse.urlparse(href)
        path = o.path
        if o.netloc == 'www.wrh.noaa.gov':
            print('skipping ' + href)
            return
        m = self.wfo_regex.match(path)
        if m is not None:
            print(m.group('wfo'))
            print(href)
            r = requests.get(href)
            doc = etree.HTML(r.content.decode('utf-8'))
            divs = doc.xpath('//div[@id="wfomap_rtcol_bot"]')
            if len(divs) == 0:
                raise RuntimeError('No wfo_rtcol_bot div')
        else:
            print('skipping ' + href)


if __name__ =='__main__':
    o = WeatherDotGov()
    o.run()
