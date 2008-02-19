from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

class WorkingArea(BrowserView):
    """
    Working Area for normal users
    """
    
    template = ViewPageTemplateFile('working_area.pt')

    def __call__(self):
        return self.template()


    def setup(self):
        pm = getToolByName(self, 'portal_membership')
        pc = getToolByName(self, 'portal_catalog')
        hf = pm.getHomeFolder()
        
        username = pm.getAuthenticatedMember().getUserName()
        self.username = username
        self.P = pc.searchResults(portal_type="RiskAssessmentLink", Creator=username)
        self.Provider = pc.searchResults(portal_type="Provider", Creator=username)
        self.home_folder = hf
        self.home_folder_url = hf and hf.absolute_url() or ''
        

    def provider(self):
        pc = getToolByName(self, 'portal_catalog')
        pm = getToolByName(self, 'portal_membership')
        username = pm.getAuthenticatedMember().getUserName()
        f = pm.getMembersFolder()
        path = "/".join( f.getPhysicalPath() ) + '/' + username
        P = pc.searchResults(portal_type="Provider", path=path)
        return len(P)>0 and P[0].getObject() or None


    def create_provider_url(self):
        if not self.home_folder:
            return ''
        href="%s/createObject?type_name=Provider" % self.home_folder_url
        return href


    def home_url(self):
        return self.home_folder_url

    def myrals(self):
        return self.P
        
    def provider_ok(self):
        return not not len(self.Provider)    