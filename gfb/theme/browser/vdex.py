from collective.dynatree.utils import dict2dynatree
from z3c.json.converter import JSONWriter
from Products.CMFCore.utils import getToolByName

class VDEXAsJson(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    def __call__(self, vdex):
        vocab_manager = getToolByName(self.context, 'portal_vocabularies')
        vocab = vocab_manager[vdex]
        vocab_dict = vocab.getVocabularyDict(self.context)
        transformed_dict = dict2dynatree(vocab_dict, [], False, False)
        return JSONWriter().write(transformed_dict)
