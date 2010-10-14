from osha.theme.browser.oshnews_view import OSHNewsLocalView
from plone.memoize import instance
import Acquisition
from Products.AdvancedQuery import Or, Eq, And, In, Le
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

class LocalNewsListing(OSHNewsLocalView):
    
    @instance.memoize
    def getResults(self):
        context = Acquisition.aq_inner(self.context)
        if context.portal_type == 'Topic':
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
