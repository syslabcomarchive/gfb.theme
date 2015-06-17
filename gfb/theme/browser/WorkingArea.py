# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from gfb.theme.browser.viewlets import GFBLanguageSelector
from Products.LinguaPlone.interfaces import ITranslatable
from plone.app.i18n.locales.browser.selector import LanguageSelector
from Products.statusmessages.interfaces import IStatusMessage
from Acquisition import aq_parent, aq_inner


class WorkingArea(GFBLanguageSelector):
    """
    Working Area for normal users
    """

    template = ViewPageTemplateFile('templates/working_area.pt')

    def __init__(self, context, request, view=None, manager=None, **args):
        super(WorkingArea, self).__init__(context, request, view, manager)
        self.context = context
        self.error = ''
        self.tool = getToolByName(context, 'portal_languages', None)
        self.pwt = getToolByName(context, 'portal_workflow')
        portal_tool = getToolByName(context, 'portal_url', None)
        self.portal_url = None
        if portal_tool is not None:
            self.portal_url = portal_tool.getPortalObject().absolute_url()

    def __call__(self):
        parent = aq_parent(aq_inner(self.context))
        status = IStatusMessage(self.request)
        if parent.getId() != "Members":
            message = "You must call the 'Workingarea' view on a member's home folder"
            status.addStatusMessage(message, type='error')
        elif self.isManager():
            pm = getToolByName(self.context, 'portal_membership')
            userid = self.context.getId()
            self.memberok = not not pm.getMemberById(userid)
            if not self.memberok:
                message = 'No user found for %s' % userid
                status.addStatusMessage(message, type='error')
        return self.template()


    def setup(self):
        pm = getToolByName(self, 'portal_membership')
        pc = getToolByName(self, 'portal_catalog')
        f = pm.getMembersFolder()

        if self.isManager():
            self.userid = self.context.getId()
            member = pm.getMemberById(self.userid)
            if not member:
                self.setError("No user found for %s" % self.userid)
                return

            self.fullname = member.getProperty('fullname')
            path = "/".join( f.getPhysicalPath() ) + '/' + self.userid
            hf = self.context.restrictedTraverse(path)
            self.home_folder = hf
            self.home_folder_url = hf and hf.absolute_url() or ''
        else:
            member = pm.getAuthenticatedMember()
            try:
                self.userid = member.getUserId()
            except:
                self.userid = member.getUserName()
            self.fullname = member.getProperty('fullname')
            path = "/".join( f.getPhysicalPath() ) + '/' + self.userid
            hf = pm.getHomeFolder()
            self.home_folder = hf
            self.home_folder_url = hf and hf.absolute_url() or ''

        self.RALinks = pc.searchResults(portal_type="RiskAssessmentLink", path=path)
        self.Provider = pc.searchResults(portal_type="Provider", path=path, Language='all')


    def setError(self, message):
        self.error = message
        self.fullname = self.userid = self.RALinks = self.Provider = self.home_folder = self.home_folder_url = ''
    @property
    def provider(self):
        provider = len(self.Provider)>0 and self.Provider[0].getObject() or None
        provider = provider and provider.getTranslation(self.tool.getPreferredLanguage()) or None
        return provider

    def providerReviewState(self):
        p = self.provider
        return p and self.pwt.getInfoFor(p, 'review_state') or ''

    @property
    def providerAddress(self):
        if self.provider:
            address = self.provider.getAddress()
            elems = list()
            for elem in address:
                if not isinstance(elem, unicode):
                    elem = elem.decode('utf-8')
                elems.append(elem)
            return u"<br>".join(elems)
        return ""

    def create_provider_url(self):
        if not self.home_folder:
            return ''
        href="%s/createObject?type_name=Provider" % self.home_folder_url
        return href


    def home_url(self):
        return self.home_folder_url

    def myrals(self):
        objs = [x.getObject() for x in self.RALinks]
        rals = [dict(obj=obj,
            state=self.pwt.getInfoFor(obj, 'review_state'),
            translation=obj.getTranslation(self.getOppositeLang(obj.Language())),
            target_language=self.getOppositeLang(obj.Language()))
            for obj in objs]
        for ral in rals:
            if ral['translation'] is not None:
                ral['translation'] = ral['translation'].absolute_url()
        return rals

    def provider_ok(self):
        return not not len(self.Provider)

    def getOppositeLang(self, lang):
        return lang in ('de', '') and 'en' or 'de'

    def getUserName(self):
        return self.fullname and self.fullname or self.userid

    def getProviderName(self):
        provider = self.provider
        return provider and provider.Title() or "n/a"

    def isManager(self):
        pm = getToolByName(self, 'portal_membership')
        member = pm.getAuthenticatedMember()
        return "Manager" in member.getRoles()


class ProviderOverview(BrowserView):

    template = ViewPageTemplateFile('templates/provider_overview.pt')

    def __call__(self):
        self.members = list()
        self.authors = list()
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        pm = getToolByName(self.context, 'portal_membership')
        mf = portal.restrictedTraverse('Members')
        for id, ob in mf.objectItems():
            if ob.portal_type != 'Folder':
                continue
            if 'workingarea' not in ob.getProperty('layout', ''):
                user = pm.getMemberById(id)
                email = user and user.getProperty('email') or ""
                self.authors.append(dict(
                    id=id, name=ob.Title(), url=ob.absolute_url(), email=email))
            else:
                providers = ob.objectValues('Provider')
                providers = [x for x in providers if x.isCanonical()]
                provider = len(providers) and providers[0].Title() or 'n/a'
                self.members.append(dict(id=id, name=ob.Title(), provider=provider,
                    url=ob.absolute_url()))
        return self.template()


class AuthorOverview(ProviderOverview):

    template = ViewPageTemplateFile('templates/author_overview.pt')
