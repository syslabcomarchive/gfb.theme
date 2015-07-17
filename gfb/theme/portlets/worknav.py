from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

class IWorkNavPortlet(IPortletDataProvider):

    pass

class Assignment(base.Assignment):
    implements(IWorkNavPortlet)

    @property
    def title(self):
        return _(u"Working Area navigation")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('worknav.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.portal = portal_state.portal()

        pm = getToolByName(self.context, 'portal_membership')
        pt = getToolByName(self.context, 'portal_url')
        self.purl = pt()
        hf = pm.getHomeFolder()
        mf = pm.getMembersFolder()
        self.home_folder = hf
        self.members_folder = mf

    # @property
    def available(self):
        return (self.isManager() or self.home_folder)

    def home_url(self):
        home_folder_url = (
            self.home_folder and self.home_folder.absolute_url() or self.purl)
        return home_folder_url

    def membersfolder_url(self):
        return self.members_folder and self.members_folder.absolute_url() or self.purl

    def getLanguage(self):
        return getToolByName(self, 'portal_languages').getPreferredLanguage()

    def isManager(self):
        pm = getToolByName(self, 'portal_membership')
        member = pm.getAuthenticatedMember()
        return "Manager" in member.getRoles()


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IWorkNavPortlet)
    label = _(u"Add WorkNav Portlet")
    description = _(u"Shows navigation for the working area.")

    def create(self):
        return Assignment()
