import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic
from gfb.theme import GFBMessageFactory as _




class AdvancedSearchView(BrowserView):
    """View for displaying the gfb search form
    It creates a search query based on the input from the template and returns the results.
    This is just another advanced search form.
    """

    template = ViewPageTemplateFile('templates/advanced_search.pt')
    template.id = "advanced_search"

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template() 

    def getFillText(self):
        """ return the translated fill text """
        label = "label_your_searchtext" 
        return _(label)

    def search_types(self):
        """ returns a list of translated search types to select from """
        context = Acquisition.aq_inner(self.context)

        local_portal_types = context.getProperty('search_portal_types', [])
        search_portal_types = self.request.get('search_portal_types', local_portal_types)
        # if all are turned off, turn them all on. Searching for nothing makes no sense.
        if not search_portal_types:
            search_portal_types = ['RiskAssessmentLink']
        TYPES = [ 
            ('Risk Assessment Link', 'RiskAssessmentLink', 'RiskAssessmentLink' in search_portal_types) ,
                ]

        return TYPES

    def get_printable_medium(self, mediumlist):
        """ returns a list of media """
        pv = getToolByName(self.context, 'portal_vocabularies')
        vocab = pv.RiskassessmentMedia
        strs = []
        dl = vocab.getDisplayList(vocab)
        for i in mediumlist:
            if not i.strip():
                continue
            val = dl.getValue(i)
            if val:
                strs.append(val)
        return strs
    

    def get_printable_method(self, methodlist):
        """ returns a translated and comma spearated string of methods """
        pv = getToolByName(self.context, 'portal_vocabularies')
        vocab = pv.RiskassessmentTypeMethodology
        strs = []
        dl = vocab.getDisplayList(vocab)
        for i in methodlist:
            if not i.strip():
                continue
            val = dl.getValue(i)
            if val:
                strs.append(val)
        return ", ".join(strs)

    def search_portal_types(self):
        """ compute the list of query params to search for portal_types"""
        context = Acquisition.aq_inner(self.context)
        #local_portal_types = context.getProperty('search_portal_types', []);
        # we need to use the output of search_types() as default, not the 
        # local Property search_portal_types
        search_types = [x[1] for x in self.search_types()]
        search_portal_types = list(self.request.get('search_portal_types', search_types))

        query = In('portal_type', search_portal_types)
        return query


    def buildQuery(self):
        """ Build the query based on the request """
        context = Acquisition.aq_inner(self.context)

        query = self.search_portal_types()

        language = getToolByName(context, 'portal_languages').getPreferredLanguage()
        query = query & In('Language', ['', language])

        nace = list(self.request.get('nace', ''))
        if '' in nace:
            nace.remove('')
        if nace:
            query = query & In('nace', nace)    

        getCategoryIndependent = self.request.get('getCategoryIndependent', '0')
        getCategoryIndependent = bool(int(getCategoryIndependent))
        query = query & Eq('getCategoryIndependent', getCategoryIndependent)


        getRemoteLanguage = self.request.get('getRemoteLanguage', '')
        if getRemoteLanguage:
            query = query & Eq('getRemoteLanguage', getRemoteLanguage)

        category = self.request.get('category', '')
        if category:
            query = query & In('category', category)    

        country = self.request.get('country', '')
        if country:
            query = query & Eq('country', country)

        provider = list(self.request.get('remote_provider', ''))
        if '' in provider:
            provider.remove('')
        if provider:
            pv = getToolByName(self, 'portal_vocabularies')
            cat = getToolByName(self, 'portal_catalog')
            VOCAB = pv.get('provider_category')
            v_dict = VOCAB and VOCAB.getVocabularyDict(self.context) or dict()
            cats = v_dict.keys()
            providerUIDs = list()
            for prov in provider:
                # if a category was selected, get all providers with that category
                if prov in cats:
                    res = cat(portal_type='Provider', getProvider_category=prov)
                    for r in res:
                        providerUIDs.append(r.UID)
                else:
                    providerUIDs.append(prov)
            query = query & In('getRemoteProviderUID', providerUIDs)

        riskfactors = self.request.get('riskfactors', '')
        if riskfactors:
            query = query & In('getRiskfactors', riskfactors)


        SearchableText = self.request.get('SearchableText', '')
        if SearchableText != '':
            query = query & Generic('SearchableText', {'query': SearchableText, 'ranking_maxhits': 10000 })

        return query
        

    def search(self):
        context = Acquisition.aq_inner(self.context)
        query = self.buildQuery()
        print query
        portal_catalog = getToolByName(context, 'portal_catalog')
        if hasattr(portal_catalog, 'getZCatalog'):
            portal_catalog = portal_catalog.getZCatalog()
        
        #return portal_catalog.evalAdvancedQuery(query, (('effective','desc'),))
        return portal_catalog.evalAdvancedQuery(query, (('modified','desc'),))
        

class HomepageSearchView(AdvancedSearchView):
    template = ViewPageTemplateFile('templates/homepage_search.pt')


class HomepageSearchNewView(AdvancedSearchView):
    template = ViewPageTemplateFile('templates/homepage_search_new.pt')

    @property
    def top_thema(self):
        #import pdb; pdb.set_trace()
        #text = 'Es wurde kein aktuelles "Top Thema" gefunden.'
        folder = getattr(self.context, "top-thema", None)
        if folder:
            path = '/'.join(folder.getPhysicalPath())
            catalog = getToolByName(self.context, 'portal_catalog')
            res = catalog(path=path, portal_type=("News Item", "Document"), review_state='published',
                sort_on="effective", sort_order="reverse")
            if len(res):
                obj = res[0].getObject()
                if obj:
                    return obj
        return None
            

    @property
    def gute_praxis(self):
        #text = 'Es wurde kein aktuelles "Besipiel guter Praxis" gefunden.'
        folder = getattr(self.context, "gute-praxis", None)
        if folder:
            path = '/'.join(folder.getPhysicalPath())
            catalog = getToolByName(self.context, 'portal_catalog')
            res = catalog(path=path, portal_type=("News Item", "Document"), review_state='published',
                sort_on="effective", sort_order="reverse")
            if len(res):
                obj = res[0].getObject()
                if obj:
                    return obj
        return None
