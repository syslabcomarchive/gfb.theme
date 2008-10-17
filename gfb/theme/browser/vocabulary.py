from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize import ram

class VocabularyPathView(BrowserView):
    """View for calculating complete paths of hierarchical vocabulary entries
    """
    def __call__(self, fieldName=''):
        field = self.context.getField(fieldName)
        if not field:
            return []

        termUID = field.getRaw(self.context)
        vocabname = field.widget.vocabulary
        
        parents_map = self.getParentsMap(vocabname)
        res = set()
        for term in termUID:
            res.update(parents_map.get(term, []) + [term])

        return list(res)


    def _getParentsMap_cachekey(method, self, vocabname):
        return (vocabname,)

    @ram.cache(_getParentsMap_cachekey)
    def getParentsMap(self, vocabname):
        pvt = getToolByName(self.context, 'portal_vocabularies')
        VOCAB = getattr(pvt, vocabname, None)
        # get the complete dictionary
        vd = VOCAB.getVocabularyDict(VOCAB)

        # the mapping holds a list of parent ids for every term id
        parents_map = dict()
        # list of current parents
        self.cp = list()

        def recurseDict(vocab_dict, level):
            for k in vocab_dict.keys():
                # clear the list of current parents for top level nodes
                if level==0:
                    self.cp = list()
                else:
                    # if it is not a root node, prune the list of current parents
                    #  ( it cannot be longer than the current level )
                    self.cp = self.cp[:level]
                    # and add the parents to the mapping
                    parents_map[k] = [x for x in self.cp]
                vd = vocab_dict[k][1]
                if vd:
                    # recurse one level deeper
                    self.cp.append(k)
                    recurseDict(vd, level+1)
        recurseDict(vd, 0)
        return parents_map
