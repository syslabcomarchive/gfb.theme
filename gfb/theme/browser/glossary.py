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
        # make sure empty letters get a notice (65-90)
        keep_track = {}
        for i in range(65,91):
            keep_track[chr(i)] = 0
        keep_track['AE'] = 0 
        keep_track['OE'] = 0 
        keep_track['UE'] = 0 
        keep_track['other'] = 0 

        for res in results:
            t = unicode(res.Title, 'utf-8')
            d = res.Description
            idx = len(t) and t[0] or u'other'
            idx = idx.upper()
            if idx == unicode('Ä', 'utf-8'): 
                idx = 'AE'
            elif idx == unicode('Ö', 'utf-8'): 
                idx = 'OE'
            elif idx == unicode('Ü', 'utf-8'): 
                idx = 'UE'
            expr = unicode('[A-Z]', 'utf-8')
            if not re.match(expr, idx):
                idx='other'
            L.append(dict(title=t, desc=d, idx=idx))
            keep_track[idx] = 1
            
        empties = [x for x in keep_track.keys() if keep_track[x]==0]
        for key in empties:
            L.append(dict(title=_('label_no_entries'), desc='', idx=key ))

        return L
