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
        vocab_dict = self.getVocabulary(vdex)
        transformed_dict = dict2dynatree(vocab_dict, [], False, False)
        return JSONWriter().write(transformed_dict)

    def getVocabulary(self, name):
        if name != 'provider':
            portal_vocabularies = getToolByName(self.context, 'portal_vocabularies')
            return portal_vocabularies[name].getVocabularyDict(self.context)
        else:
            util = getUtility(IVocabularyUtility, name)
            return util.getVocabularyDict()
