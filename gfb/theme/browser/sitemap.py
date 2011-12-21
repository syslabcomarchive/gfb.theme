# -*- coding: utf-8 -*-
from plone.app.layout.sitemap.sitemap import SiteMapView as BaseView
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
from zope.publisher.interfaces import NotFound
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime import DateTime
from types import *
from gzip import GzipFile
from cStringIO import StringIO
import urlparse
from Products.AdvancedQuery import Eq, In, And, Or

from plone.memoize import ram

MAX_SIZE = 1024*1024*9
FILE_IDX = 'sitemap_index.xml.gz'
FILE_PART = "sitemap_%s.xml.gz"



class NewsMapView(BaseView):
    """Creates the newsmap as explained in the specifications.

    http://www.google.com/support/webmasters/bin/answer.py?answer=42738
    """

    template = ViewPageTemplateFile('templates/newsmap.xml')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.filename = 'newsmap_en.xml.gz'


    def __call__(self):
        """Checks if the sitemap feature is enable and returns it."""
        sp = getToolByName(self.context, 'portal_properties').site_properties
        if not sp.enable_sitemap:
            raise NotFound(self.context, self.filename, self.request)

        self.request.response.setHeader('Content-Type',
                                        'application/octet-stream')
        return self.generate()


    def generate(self):
        """Generates the Gzipped sitemap."""
        xml = self.template()
        fp = StringIO()
        gzip = GzipFile(self.filename, 'w', 9, fp)
        gzip.write(xml)
        gzip.close()
        data = fp.getvalue()
        fp.close()
        return data

    def objects(self):
        """Returns the data to create the sitemap."""
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_url = getToolByName(self.context, 'portal_url')
        portal_path = portal_url.getPortalPath()
        if hasattr(catalog, 'getZCatalog'):
            catalog = catalog.getZCatalog()
        portal_url = getToolByName(self.context, 'portal_url')

        query = Eq('Language', 'en') & Eq('review_state', 'published') \
            & In('portal_type', ['News Item', 'PressRelease']) \
            & ~Eq('outdated', True)
        paths = In('path', ['%s/en/teaser'%portal_path, '%s/en/press'%portal_path])
        query = query & paths


        results = catalog.evalAdvancedQuery(query)[:1000]
        for item in results:
            try:
                lastmod = item.modified.ISO8601()
            except:
                lastmod = '2008-01-01T1:00:00+00:00'

            loc = item.getURL()

            changefreq = item.get('changefreq', "monthly")
            priority = item.get('priority', 0.9)
            if item.effective<(DateTime()-30):
                priority = 0.3
            else:
                priority = 0.9
            keywords = [x for x in item.Subject if x is not None]
            keywords = ",".join(keywords)

            try:
                publication_date = item.effective.ISO8601()
            except:
                publication_date = '2008-01-01T1:00:00+00:00'

            yield {
                'loc': loc,
                'lastmod': lastmod,
                'changefreq': changefreq, # hourly/daily/weekly/monthly/yearly/never
                'priority': priority, # 0.0 to 1.0
                'keywords': keywords,
                'publication_date': publication_date
            }


def _render_cachekey(fun, self):
    # Cache by filename
    url_tool = getToolByName(self.context, 'portal_url')
    return '%s/%s' % (url_tool(), self.filename)

class SiteMapView(BaseView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """

    template = ViewPageTemplateFile('templates/sitemap.xml')
    link_snippet = ViewPageTemplateFile('templates/sitemap_link.xml')
    env_snippet = ViewPageTemplateFile('templates/sitemap_envelope.xml')
    index_snippet = ViewPageTemplateFile('templates/sitemap_index.xml')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.filename = 'sitemap.xml.gz'
        self.urlmap = self.parseUrlFile()

    def __call__(self):
        """Checks if the sitemap feature is enable and returns it."""
        sp = getToolByName(self.context, 'portal_properties').site_properties
        if not sp.enable_sitemap:
            raise NotFound(self.context, self.filename, self.request)

        self.request.response.setHeader('Content-Type',
                                        'application/octet-stream')
        return self.generate()

    def persistFiles(self, objects):
        """ write the map into a file object to avoid google download timeouts """
        portal_url = getToolByName(self.context, 'portal_url')
        purl = portal_url()
        now = DateTime().ISO8601()
        total_len = 0
        counter = 0
        LINKS = ""
        filenames = []
        for ob in objects:
            xml = self.link_snippet(obj=ob)
            LINKS += xml

            if len(LINKS)>MAX_SIZE and LINKS != "":
                counter +=1
                part_name = FILE_PART % counter
                self._persist_file(part_name, self.env_snippet(LINKS=LINKS))
                filenames.append("%s/%s" %(purl, part_name))
                LINKS = ''
                total_len = 0

        counter +=1
        part_name = FILE_PART % counter
        self._persist_file(part_name, self.env_snippet(LINKS=LINKS))
        filenames.append("%s/%s" %(purl, part_name))

        snip = self.index_snippet(filenames=filenames, now=now)
        data = self._persist_file(FILE_IDX, snip)
        return data

    def parseUrlFile(self):
        """ parses a simple file with format url,changefreq,priority """
        urlfile = getattr(self.context, 'sitemap_urlfile', None)
        if urlfile is None:
            return {}
        urldata = str(urlfile.data)
        urlmap = {}
        for line in urldata.split("\n"):
            elems = line.split(",")
            if len(elems)>2:
                urlmap[elems[0].strip()] = (elems[1].strip(), elems[2].strip())

        return urlmap

    def _persist_file(self, filename, data):
        """ persists a file to the site root """
        site = getSite()
        data = self._make_zip(filename, data)
        if filename not in site.objectIds():
            site.manage_addFile(filename)
        F = getattr(site, filename)
        F.update_data(data)
        F.content_type='application/octet-stream'
        return data


    def _make_zip(self, filename, data):
        """ generates a zipfile from data """
        fp = StringIO()
        gzip = GzipFile(filename, 'w', 9, fp)
        gzip.write(data)
        gzip.close()
        data = fp.getvalue()
        fp.close()
        return data


    #@ram.cache(_render_cachekey)
    def generate(self):
        """Generates the Gzipped sitemap."""
        objects = self.objects()
        data = self.persistFiles(objects)
        return data

    def objects(self):
        """Returns the data to create the sitemap."""
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_url = getToolByName(self.context, 'portal_url')

        # the main url does not turn up as a catalog result so we do it manually
        yield {
            'loc': portal_url(),
            'lastmod': DateTime().ISO8601(),
            'changefreq': 'always',
            'priority': 1
        }

        for item in catalog.searchResults({'Language': 'all', 'review_state': 'published'}):
            # We only want to link them in the search form results
            if item.portal_type in ['Amendment', 'Modification', 'Note', 'Proposal', 'LinguaLink']:
                continue
            try:
                lastmod = item.modified.ISO8601()
            except:
                lastmod = '2008-01-01T1:00:00+00:00'

            loc = item.getURL()

            changefreq = item.get('changefreq', "monthly")
            priority = item.get('priority', 0.3)

            if item.portal_type in ['Event', 'News Item']:
                changefreq = "never"
            if item.effective<(DateTime()-30):
                priority = 0.3
            else:
                priority = 0.9

            # manually set urlmap overrides
            if self.urlmap.has_key(loc):
                changefreq, priority = self.urlmap[loc]

            yield {
                'loc': loc,
                'lastmod': lastmod,
                'changefreq': changefreq, # hourly/daily/weekly/monthly/yearly/never
                'priority': priority, # 0.0 to 1.0
            }

