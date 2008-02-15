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


    @property
    def available(self):
        return self._data()

    @memoize
    def _data(self):
        return True

    def home_url(self):
        pm = getToolByName(self, 'portal_membership')
        pt = getToolByName(self, 'portal_url')
        hf = pm.getHomeFolder()
        self.home_folder = hf
        home_folder_url = hf and hf.absolute_url() or pt()
        return home_folder_url


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IWorkNavPortlet)
    label = _(u"Add WorkNav Portlet")
    description = _(u"Shows navigation for the working area.")

    def create(self):
        return Assignment()
