from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.app.layout.icons.icons import CatalogBrainContentIcon


class CatalogBrainContentIconWithTitle(CatalogBrainContentIcon):

    @property
    def title(self):
        context = aq_inner(self.context)
        tt = getToolByName(context, 'portal_types')
        portal_type = self.brain.get("portal_type")
        fti = tt.get(portal_type)
        lt = getToolByName(self.context, 'portal_languages')
        lang = lt.getPreferredLanguage()

        if fti is not None:
            return context.translate(
                domain="plone",
                msgid=fti.Title(),
                default=fti.Title(),
                target_language=lang,
            )
        else:
            return portal_type
