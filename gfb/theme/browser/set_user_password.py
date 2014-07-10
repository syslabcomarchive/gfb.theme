from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from gfb.theme import GFBMessageFactory as _
from Products.CMFPlone import PloneMessageFactory as pmf


class SetUserPasswordView(BrowserView):

    def __call__(self):
        form = self.request.form
        userid = form.get("userid", None)
        password1 = form.get("password1", None)
        password2 = form.get("password2", None)
        messages = IStatusMessage(self.request)
        registration = getToolByName(self.context, 'portal_registration')

        if userid is None:
            messages.add(_('No user has been specified'), "error")
        elif password1 is password2 is None:
            return self.index()
        else:
            mt = getToolByName(self.context, "portal_membership")
            member = mt.getMemberById(userid)
            if member is None:
                messages.add(_('Invalid user id'), "error")
            else:
                fail_message = registration.testPasswordValidity(
                    password1, password2)
                if fail_message:
                    messages.add(pmf(fail_message), "error")
                else:
                    member.setSecurityProfile(password=password1)
                    messages.add(pmf("Password changed"), "info")
        return self.index()
