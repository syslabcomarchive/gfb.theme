from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName


class IMyRALPortlet(IPortletDataProvider):

    pass

class Assignment(base.Assignment):
    implements(IMyRALPortlet)

    @property
    def title(self):
        return _(u"My Risk Assessment Links")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('myral.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')

        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()

    def myrals(self):
        pm = getToolByName(self, 'portal_membership')
        hf = pm.getHomeFolder()
        if not hf:
            return None
        P = hf.getFolderContents({'portal_type': 'RiskAssessmentLink'})
        return P

    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IMyRALPortlet)
    label = _(u"Add MyRAL Portlet")
    description = _(u"Lists all Risk Assessment Links in the current members homefolder.")

    def create(self):
        return Assignment()
