import Acquisition, re
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic
from gfb.theme import GFBMessageFactory as _




class GlossaryView(BrowserView):
    """View for displaying the gfb search form
    It creates a search query based on the input from the template and returns the results.
    This is just another advanced search form.
    """

    template = ViewPageTemplateFile('templates/glossary.pt')
    template.id = "gfb_glossary"

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template() 


    def buildQuery(self):
        """ Build the query based on the request """
        context = Acquisition.aq_inner(self.context)
        query = In('portal_type', 'HelpCenterDefinition') & Eq('review_state', 'published')
        return query
        

    def data(self):
        context = Acquisition.aq_inner(self.context)
        query = self.buildQuery()
        portal_catalog = getToolByName(context, 'portal_catalog')
        if hasattr(portal_catalog, 'getZCatalog'):
            portal_catalog = portal_catalog.getZCatalog()
        
        results = portal_catalog.evalAdvancedQuery(query, (('sortable_title','asc'),))

        L = []
        for res in results:
            t = unicode(res.Title, 'utf-8')
            d = res.Description
            idx = len(t) and t[0] or u'other'
            idx = idx.upper()
#            if idx == u'Ä': 
#                idx = 'AE'
#            elif idx == u'Ö': 
#                idx = 'OE'
#            elif idx == u'Ü': 
#                idx = 'UE'
            expr = unicode('[ÄÖÜA-Z]', 'utf-8')
            if not re.match(expr, idx):
                import pdb;pdb.set_trace()
                idx='other'
            L.append(dict(title=t, desc=d, idx=idx))
    
        return L
