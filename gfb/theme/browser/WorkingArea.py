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
        
        try:
            self.userid = pm.getAuthenticatedMember().getUserId()
        except:
            self.userid = pm.getAuthenticatedMember().getUserName()
        f = pm.getMembersFolder()
        path = "/".join( f.getPhysicalPath() ) + '/' + self.userid
        self.P = pc.searchResults(portal_type="RiskAssessmentLink", path=path)
        self.Provider = pc.searchResults(portal_type="Provider", path=path, Language='all')

        hf = pm.getHomeFolder()
        self.home_folder = hf
        self.home_folder_url = hf and hf.absolute_url() or ''
        

    def provider(self):
        return len(self.Provider)>0 and self.Provider[0].getObject() or None

    def providerReviewState(self):
        p = self.provider()
        pw = getToolByName(self, 'portal_workflow')
        return p and pw.getInfoFor(p, 'review_state') or ''
        

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