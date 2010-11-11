from Acquisition import aq_inner, aq_base, aq_parent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from plone.app.layout.viewlets.content import DocumentActionsViewlet
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from webcouturier.dropdownmenu.browser.dropdown import DropdownMenuViewlet
from plone.app.portlets.portlets.navigation import Assignment
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.app.portlets.cache import get_language
#from plone.app.i18n.locales.browser.selector import LanguageSelector 
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector


from zope.component import getMultiAdapter
from Products.CMFPlone.utils import safe_unicode
from cgi import escape


#Overwrite Languageselector to customize appearance
class GFBLanguageSelector(TranslatableLanguageSelector):
    render = ViewPageTemplateFile('templates/languageselector.pt')

    def isSpecialFish(self):
        """ Method that returns true if the language selector should be displayed
        even if the object is not translated.
        This is the case for the Members folder"""
        try:
            parent = aq_parent(aq_inner(self.context))
            if parent.id == 'Members':
                return True
        except:
            pass
        return False


# Overwrite PersonalBarViewlet
class PersonalBarViewletGFB(common.PersonalBarViewlet):
    render = ViewPageTemplateFile('personal_bar_gfb.pt')


class EditHelp(common.ViewletBase):
    render = ViewPageTemplateFile('editing_help.pt')
    
class SiteTitleViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/site_title.pt')
    
    
class PathBarViewletGFB(common.PathBarViewlet):
    render = ViewPageTemplateFile('templates/path_bar.pt')

class GlobalSectionsViewletGFB(DropdownMenuViewlet, common.GlobalSectionsViewlet, common.SearchBoxViewlet):
    render = ViewPageTemplateFile('templates/sections.pt')

    def update(self):
        # from viewletbase                
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()

        # from dropdownmenu
        super(DropdownMenuViewlet, self).update()
        self.properties = getToolByName(self.context, 'portal_properties').navtree_properties
        self.data = Assignment()


        # from globalsections
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        actions = context_state.actions()
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)

        selectedTabs = self.context.restrictedTraverse('selectedTabs')
        self.selected_tabs = selectedTabs('index_html',
                                          self.context,
                                          self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']


        # from searchbox
        props = getToolByName(self.context, 'portal_properties')
        livesearch = props.site_properties.getProperty('enable_livesearch', False)
        if livesearch:
            self.search_input_id = "searchGadget"
        else:
            self.search_input_id = ""

        folder = context_state.folder()
        self.folder_path = '/'.join(folder.getPhysicalPath())
        
        
    def search_site_url(self):
        langtool = getToolByName(self.context, 'portal_languages')
        preflang = langtool.getPreferredLanguage()
        return "%s/%s" %(self.site_url, preflang)
        
class FooterActions(common.ViewletBase):
    
    _template = ViewPageTemplateFile('templates/footer_actions.pt')
    
    
    
    def _footer_render_details_cachekey(fun, self):
        """
        Generates a key based on:
    
        * Current URL
        * Negotiated language
        * Anonymous user flag
        
        """
        context = aq_inner(self.context)
    
        anonymous = getToolByName(context, 'portal_membership').isAnonymousUser()
    
        key= "".join((
            '/'.join(aq_inner(self.context).getPhysicalPath()),
            get_language(aq_inner(self.context), self.request),
            str(anonymous),
            ))
        return key    
    
    
    @ram.cache(_footer_render_details_cachekey) 
    def render(self):
        return xhtml_compress(self._template())

    def update(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')    
                                            
        self.portal = portal_state.portal() 
        self.site_url = portal_state.portal_url()                                   
                                        
        self.portal_actionicons = aq_base(getToolByName(self.context, 'portal_actionicons'))
                                                
        self.footer_actions = context_state.actions().get('footer_actions', None)        
        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor

    def icon(self, action):
        return self.getIconFor('plone', action['id'], None)


class GFBTitleViewlet(common.TitleViewlet):

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.page_title = self.context_state.object_title
        self.portal_title = self.portal_state.portal_title

    def index(self):
        portal_title = safe_unicode(self.portal_title())
        page_title = safe_unicode(self.page_title())
        if page_title == portal_title:
            return u"<title>%s</title>" % (escape(portal_title))
        else:
            return u"<title>%s &mdash; %s</title>" % (
                escape(safe_unicode(portal_title)),
                escape(safe_unicode(page_title))
                )


class GFBDocumentActionsViewlet(DocumentActionsViewlet):

    index = ViewPageTemplateFile('templates/document_actions.pt')

    def getLink(self):
        context = self.context
        link = context.request.get('ACTUAL_URL') + \
            (context.request.get('QUERY_STRING') and '?' + context.request.get('QUERY_STRING') or '')
        return link


class GFBLogoViewlet(common.LogoViewlet):

    index = ViewPageTemplateFile('templates/logo.pt')


class GFBSkipLinksViewlet(common.SkipLinksViewlet):

    index = ViewPageTemplateFile('templates/skip_links.pt')


class GFBSiteActionsViewlet(common.SiteActionsViewlet):
    index = ViewPageTemplateFile('templates/site_actions.pt')
