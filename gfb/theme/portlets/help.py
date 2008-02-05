from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

class IHelpPortlet(IPortletDataProvider):

    pass

class Assignment(base.Assignment):
    implements(IHelpPortlet)

    @property
    def title(self):
        return _(u"Help")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('help.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')

        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()

    def help_document(self):
        H = getattr(self.portal, 'dashboard_help', None)
        
        return H

    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IHelpPortlet)
    label = _(u"Add Help Portlet")
    description = _(u"Shows information on how to use the GFB portal.")

    def create(self):
        return Assignment()
