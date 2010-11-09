from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from Products.LinguaPlone.interfaces import ITranslatable
from plone.app.i18n.locales.browser.selector import LanguageSelector
from Products.statusmessages.interfaces import IStatusMessage
from Acquisition import aq_parent, aq_inner

class WorkingArea(BrowserView, TranslatableLanguageSelector):
    """
    Working Area for normal users
    """
    
    template = ViewPageTemplateFile('templates/working_area.pt')

    def __init__(self, context, request, **args):
        super(WorkingArea, self).__init__(context, request)
        self.context = context
        self.tool = getToolByName(context, 'portal_languages', None)
        self.pwt = getToolByName(context, 'portal_workflow')
        portal_tool = getToolByName(context, 'portal_url', None)
        self.portal_url = None
        if portal_tool is not None:
            self.portal_url = portal_tool.getPortalObject().absolute_url()

    def __call__(self):
        return self.template()

    def getTemplateName(self):
        return "workingarea"

    def languages(self):
        results = LanguageSelector.languages(self)
        translatable = ITranslatable(self.context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = []

        for data in results:
            data['translated'] = data['code'] in translations
            if data['translated']:
                trans = translations[data['code']][0]
                state = getMultiAdapter((trans, self.request),
                        name='plone_context_state')
                data['url'] = state.view_url() + '/' + self.getTemplateName() + '?set_language=' + data['code']
            else:
                state = getMultiAdapter((self.context, self.request),
                        name='plone_context_state')
                try:
                    data['url'] = state.view_url() + '/' + self.getTemplateName() + '?set_language=' + data['code']
                except AttributeError:
                    data['url'] = self.context.absolute_url() + '/' + self.getTemplateName()  + '?set_language=' + data['code']

        return results

    def setup(self):
        pm = getToolByName(self, 'portal_membership')
        pc = getToolByName(self, 'portal_catalog')
        
        member = pm.getAuthenticatedMember()
        try:
            self.userid = member.getUserId()
        except:
            self.userid = member.getUserName()
        self.fullname = member.getProperty('fullname')
        f = pm.getMembersFolder()
        path = "/".join( f.getPhysicalPath() ) + '/' + self.userid
        self.RALinks = pc.searchResults(portal_type="RiskAssessmentLink", path=path)
        self.Provider = pc.searchResults(portal_type="Provider", path=path, Language='all')

        hf = pm.getHomeFolder()
        self.home_folder = hf
        self.home_folder_url = hf and hf.absolute_url() or ''
        

    def provider(self):
        return len(self.Provider)>0 and self.Provider[0].getObject() or None

    def providerReviewState(self):
        p = self.provider()
        return p and self.pwt.getInfoFor(p, 'review_state') or ''
        

    def create_provider_url(self):
        if not self.home_folder:
            return ''
        href="%s/createObject?type_name=Provider" % self.home_folder_url
        return href


    def home_url(self):
        return self.home_folder_url

    def myrals(self):
        objs = [x.getObject() for x in self.RALinks]
        return [dict(obj=obj,
            state=self.pwt.getInfoFor(obj, 'review_state'),
            translation=obj.getTranslation(self.getOppositeLang(obj.Language())),
            target_language=self.getOppositeLang(obj.Language()))
            for obj in objs]
        
    def provider_ok(self):
        return not not len(self.Provider)

    def getOppositeLang(self, lang):
        return lang in ('de', '') and 'en' or 'de'

    def getUserName(self):
        return self.fullname and self.fullname or self.userid

    def getProviderName(self):
        provider = self.provider()
        return provider and provider.Title() or "n/a"


class WorkingAreaManager(WorkingArea):
    """ Working Area that does not force the view to the currently logged in
        user's home folder, but displays the content of any user folder."""

    def __init__(self, context, request, **args):
        super(WorkingAreaManager, self).__init__(context, request)
        self.error = ''
        self.userid = self.request.get('userid', '')
        if not self.userid:
            try:
                self.userid = aq_parent(aq_inner(self.context)).getId() == 'Members' and \
                    self.context.getId() or ''
            except:
                pass
        pm = getToolByName(context, 'portal_membership')
        if self.userid:
            self.memberok = not not pm.getMemberById(self.userid)
            if not self.memberok:
                self.error = 'No user found for %s' %self.userid
        else:
            self.error = "You must provide a userid as parameter or call the view on a member folder"
            self.memberok = False


    def getTemplateName(self):
        return "workingarea-manager"

    def setup(self):
        if self.memberok:
            pc = getToolByName(self.context, 'portal_catalog')
            pm = getToolByName(self.context, 'portal_membership')
            member = pm.getMemberById(self.userid)
            self.fullname = member.getProperty('fullname')
            f = pm.getMembersFolder()
            path = "/".join( f.getPhysicalPath() ) + '/' + self.userid
            self.RALinks = pc.searchResults(portal_type="RiskAssessmentLink", path=path)
            self.Provider = pc.searchResults(portal_type="Provider", path=path, Language='all')

            hf = self.context.restrictedTraverse(path)
            self.home_folder = hf
            self.home_folder_url = hf and hf.absolute_url() or ''
        else:
            self.fullname = self.userid = self.RALinks = self.Provider = self.home_folder = self.home_folder_url = ''


    def __call__(self):
        if self.error:
            status = IStatusMessage(self.request)
            status.addStatusMessage(self.error, type='error')
        return self.template()


class ProviderOverview(BrowserView):

    template = ViewPageTemplateFile('templates/provider_overview.pt')

    def __call__(self):
        return self.template()

    def getMembers(self):
        members = list()
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        mf = portal.restrictedTraverse('Members')
        for id, ob in mf.objectItems('ATFolder'):
            providers = ob.objectValues('Provider')
            providers = [x for x in providers if x.isCanonical()]
            provider = len(providers) and providers[0].Title() or 'n/a'
            members.append(dict(id=id, name=ob.Title(), provider=provider,
                url=ob.absolute_url()))

        return members
  