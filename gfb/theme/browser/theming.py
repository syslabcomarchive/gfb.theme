# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.layout.globals import layout


class LayoutPolicy(layout.LayoutPolicy):

    def bodyClass(self, template, view):
        """Returns the CSS class to be used on the body tag."""

        body_class = super(LayoutPolicy, self).bodyClass(template, view)

        mtool = getToolByName(self.context, 'portal_membership')
        if not mtool.isAnonymousUser():
            if mtool.checkPermission('Manage portal', self.context):
                body_class += " is-manager"
            else:
                body_class += " is-not-manager"

        return body_class
