from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase, PersonalBarViewlet

# Overwrite PersonalBarViewlet
class PersonalBarViewletGFB(PersonalBarViewlet):
    render = ViewPageTemplateFile('personal_bar_gfb.pt')


class EditHelp(ViewletBase):
    render = ViewPageTemplateFile('editing_help.pt')