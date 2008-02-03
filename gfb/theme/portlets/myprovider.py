from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

class IMyProviderPortlet(IPortletDataProvider):

    pass

class Assignment(base.Assignment):
    implements(IMyProviderPortlet)

    @property
    def title(self):
        return _(u"Provider Overview")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('myprovider.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')

        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()

    def provider(self):
        pm = getToolByName(self, 'portal_membership')
        hf = pm.getHomeFolder()
        if not hf:
            return None
        P = hf.getFolderContents({'portal_type': 'Provider'})
        return len(P)>0 and P[0] or None

    def create_url(self):
        pm = getToolByName(self, 'portal_membership')
        hf = pm.getHomeFolder()
        if not hf:
            return ''
        href="%s/createObject?type_name=Provider" % hf.absolute_url()
        return href

    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IMyProviderPortlet)
    label = _(u"Add MyProvider Portlet")
    description = _(u"Shows information about the current logged in users provider data.")

    def create(self):
        return Assignment()
