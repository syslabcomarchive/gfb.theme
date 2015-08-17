# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.layout.globals import layout
from zope.component import getMultiAdapter


class LayoutPolicy(layout.LayoutPolicy):

    def bodyClass(self, template, view):
        """Returns the CSS class to be used on the body tag."""

        body_class = super(LayoutPolicy, self).bodyClass(template, view)

        mtool = getToolByName(self.context, 'portal_membership')
        if not mtool.isAnonymousUser():
            if not mtool.checkPermission('Manage portal', self.context):
                pwt = getToolByName(self.context, 'portal_workflow')
                if pwt.getInfoFor(self.context, 'review_state', '') == 'private':
                    iterate_control = getMultiAdapter(
                        (self.context, self.request), name='iterate_control')
                    if iterate_control.cancel_allowed():
                        body_class += " hide-content-actions"
            if mtool.checkPermission('Modify portal content', self.context):
                body_class += " can-modify"
            else:
                body_class += " cannot-modify"
        return body_class
