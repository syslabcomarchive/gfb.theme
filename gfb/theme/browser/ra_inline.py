# -*- coding: utf-8 -*-
from Acquisition import aq_base, aq_inner
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class RAInlineView(BrowserView):
    """View for displaying ra links fetched by UID in the current context
    """

    def __call__(self):
        self.request.set('disable_border', True)
        uid = self.request.get('uid', None)
        if uid is None:
            self.request.RESPONSE.badRequestError('uid')
        # guard against wrong formatting of the query string, such as
        # ra_inline?uid=ff07dd4c2126f5540d882a78dbbfc665/?searchterm=None
        # A slash can never be part of the UID, so we should be safe here
        uid = uid.split('/')[0]
        pc = getToolByName(self.context, 'portal_catalog')
        results = pc(UID=uid)
        if len(results) != 1:
            self.request.RESPONSE.badRequestError('uid')
        result = results[0]
        ob = result.getObject()

        # put the object in current context
        wrapped_ob = aq_inner(aq_base(ob)).__of__(self.context)

        return wrapped_ob()
