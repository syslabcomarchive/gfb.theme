# -*- coding: utf-8 -*-
from plone.app.users.browser.register import AddUserForm as BaseAddUserForm
from zope import schema
from zope.formlib import form
from zope.interface import Interface


class IAddUserSchema(Interface):

    is_expert_author = schema.Bool(
        title=u"Ist der Nutzer ein Autor für den Bereich Expertenwissen?",
        default=False)


class AddUserForm(BaseAddUserForm):

    @property
    def form_fields(self):
        default_fields = super(AddUserForm, self).form_fields

        # Append the manager-focused fields
        all_fields = default_fields + form.Fields(IAddUserSchema)
        return all_fields
