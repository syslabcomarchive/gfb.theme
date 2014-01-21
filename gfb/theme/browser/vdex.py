from collective.dynatree.utils import dict2dynatree
from z3c.json.converter import JSONWriter
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from gfb.policy.interfaces import IVocabularyUtility


class VDEXAsJson(object):

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def __call__(self, vdex):
        if vdex != 'provider':
            tool = getToolByName(self.context, 'portal_vocabularies')
            vocab_dict = tool[vdex].getVocabularyDict(self.context)
        else:
            util = getUtility(IVocabularyUtility, vdex)
            vocab_dict = util.getVocabularyDict()
        if vdex == 'NACE':
            showKey = True
        else:
            showKey = False

        transformed_dict = dict2dynatree(vocab_dict, [], False, showKey)
        
        self.request.RESPONSE.setHeader('Cache-control', 'max-age=84600,s-maxage=84600s')
        
        return JSONWriter().write(transformed_dict)
