# -*- coding: utf-8 -*-
import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic
from gfb.theme import GFBMessageFactory as _


class RAInlineView(BrowserView):
    """View for displaying ra links fetched by UID in the current context
    """

    def __call__(self):
        self.request.set('disable_border', True)
        uid = self.request.get('uid', None)
        if uid is None:
            raise NotFound
        # guard against wrong formatting of the query string, such as
        # ra_inline?uid=ff07dd4c2126f5540d882a78dbbfc665/?searchterm=None
        # A slash can never be part of the UID, so we should be safe here
        uid = uid.split('/')[0]
        pc = getToolByName(self.context, 'portal_catalog')
        results = pc(UID=uid)
        if len(results)!=1:
            self.request.RESPONSE.badRequestError('uid')
        result = results[0]
        ob = result.getObject()

        #put the object in current context
        N = Acquisition.aq_inner(Acquisition.aq_base(ob)).__of__(self.context)
        # save the original object's path - needed for correct linking of actions
        setattr(N, 'original_url_path', ob.absolute_url_path())

        return N()

