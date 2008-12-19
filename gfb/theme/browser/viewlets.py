from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase, PersonalBarViewlet, PathBarViewlet, GlobalSectionsViewlet, SearchBoxViewlet

# Overwrite PersonalBarViewlet
class PersonalBarViewletGFB(PersonalBarViewlet):
    render = ViewPageTemplateFile('personal_bar_gfb.pt')


class EditHelp(ViewletBase):
    render = ViewPageTemplateFile('editing_help.pt')
    
class SiteTitleViewlet(ViewletBase):
    render = ViewPageTemplateFile('templates/site_title.pt')
    
    
class PathBarViewletGFB(PathBarViewlet):
    render = ViewPageTemplateFile('templates/path_bar.pt')

class GlobalSectionsViewletGFB(GlobalSectionsViewlet):
    render = ViewPageTemplateFile('templates/sections.pt')

class SearchBoxViewletGFB(SearchBoxViewlet):
    render = ViewPageTemplateFile('templates/searchbox.pt')