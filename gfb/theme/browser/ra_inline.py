import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic
from gfb.theme import GFBMessageFactory as _




class RAInlineView(BrowserView):
    """View for displaying ra links fetched by UID in the current context
    """
    #template = ViewPageTemplateFile('templates/ra_inline.pt')
    #template.id = "ra_inline"

    def __call__(self):
        self.request.set('disable_border', True)
        uid = self.request.get('uid', None)
        if uid is None:
            raise NotFound
        if len(uid)>32:
            uid = uid[:32]  #cropping searchtext= away
        pc = getToolByName(self.context, 'portal_catalog')
        results = pc(UID=uid)
        assert len(results)==1
        result = results[0]
        ob = result.getObject()

        #put the object in current context
        N = Acquisition.aq_inner(Acquisition.aq_base(ob)).__of__(self.context)
        return N()

