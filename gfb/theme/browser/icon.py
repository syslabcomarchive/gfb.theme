from zope.interface import implements
from Acquisition import aq_inner
from Products.CMFCore.utils  import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.icons.interfaces import IContentIcon
from plone.app.layout.icons.icons import BaseIcon
from plone.app.layout.icons.icons import CatalogBrainContentIcon
from plone.app.layout.icons.icons import DefaultContentIcon
from zope.component import getMultiAdapter


class ContentIconWithTitle(DefaultContentIcon):
    """ #9044 set the icon title to the portal_type
    """
    implements(IContentIcon)

    @property
    def title(self):
        context = aq_inner(self.context)
        tt = getToolByName(context, 'portal_types')
        fti = tt.get(self.obj['portal_type'])
        if fti is not None:
            return fti.Title()
        else:
            return self.obj['portal_type']

    @property
    def description(self):
        if self.obj is None:
            return None
        return safe_unicode(self.obj.Title)

    @property
    def url(self):
        path = self.obj.getIcon
        if not path:
            return path

        portal_state_view = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        portal_url = portal_state_view.portal_url()
        return "%s/%s" % (portal_url, path)
