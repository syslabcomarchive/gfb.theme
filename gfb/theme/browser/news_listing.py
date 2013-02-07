# -*- coding: utf-8 -*-
from plone.memoize import instance
import Acquisition
from Products.AdvancedQuery import Or, Eq, And, In, Le
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.ATContentTypes.interface import IATTopic
from gfb.theme import GFBMessageFactory as _


class LocalNewsListing(BrowserView):

    def __call__(self):
        return self.index()

    def getName(self):
        return self.__name__

    def Title(self):
        context = Acquisition.aq_inner(self.context)
        if IATTopic.providedBy(context):
            return context.Title()
        return _(u"heading_newsboard_latest_news")

    #@instance.memoize
    def getResults(self):
        context = Acquisition.aq_inner(self.context)
        if IATTopic.providedBy(context):
            results = context.queryCatalog()
        else:
            catalog = getToolByName(context, 'portal_catalog')
            if hasattr(catalog, 'getZCatalog'):
                catalog = catalog.getZCatalog()

            now = DateTime()
            queryA = Eq('portal_type', 'News Item')
            queryBoth = In('review_state', 'published') & Eq('path', '/'.join(context.getPhysicalPath())) \
                & Le('effective', now)

            query = And(queryA, queryBoth)
            results = catalog.evalAdvancedQuery(query, (('Date', 'desc'),) )

        return results

    def queryCatalog(self, b_size=20):
        results = self.getResults()
        b_start = self.request.get('b_start', 0)
        batch = Batch(results, b_size, int(b_start), orphan=0)
        return batch

    def getBodyText(self):
        """ returns body text of collection  if present """
        context = Acquisition.aq_base(Acquisition.aq_inner(self.context))
        text = getattr(context, 'getText', None) and context.getText() or ''
        return text

    def showLinkToNewsItem(self):
        return self.context.getProperty('show_link_to_news_item', True)

