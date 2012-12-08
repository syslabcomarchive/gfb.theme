from BeautifulSoup import BeautifulSoup
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from gfb.theme.browser.interfaces import IGFB
import Acquisition


class GFB(BrowserView):
    implements(IGFB)

    def cropHTMLText(self, text, length, ellipsis=u'...'):
        """ first strip html, then crop """
        context = Acquisition.aq_inner(self.context)
        portal_transforms = getToolByName(context, 'portal_transforms')
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        try:
            text = portal_transforms.convert('html_to_text', text).getData()
            text = text.decode('utf-8')
        except Exception, err:
            logger.error('An error occurred in cropHTMLText, original text: %s, message: %s ' \
                'URL: %s' % (str([text]), str(err), context.absolute_url()))
            return text
        return context.restrictedTraverse('@@plone').cropText(text, length,
            ellipsis)

