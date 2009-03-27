import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic
from gfb.theme import GFBMessageFactory as _




class GlossaryView(BrowserView):
    """View for displaying the gfb search form
    It creates a search query based on the input from the template and returns the results.
    This is just another advanced search form.
    """

    template = ViewPageTemplateFile('templates/glossary.pt')
    template.id = "gfb_glossary"

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template() 






    def buildQuery(self):
        """ Build the query based on the request """
        context = Acquisition.aq_inner(self.context)

        query = self.search_portal_types()

        #query = { 'sort_on': 'effective',
        #          'sort_order':'reverse',
        #          'Language': ''}
        language = getToolByName(context, 'portal_languages').getPreferredLanguage()
        query = query & In('Language', ['', language])

#        keywords = self.request.get('keywords', [])
#        if keywords:
#            query = query & In('Subject', keywords)
#            #query.update({'Subject':keywords})

        nace = list(self.request.get('nace', ''))
        if '' in nace:
            nace.remove('')
        if nace:
            query = query & In('nace', nace)    

        getCategoryIndependent = self.request.get('getCategoryIndependent', '1')
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
            cats = VOCAB and VOCAB.keys() or list()
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
        
