from Products.CMFCore.utils import getToolByName
from plone.app.iterate.browser.diff import DiffView as BaseDiffView


SKIP_FIELDS = [
    'getId',
    'Subject',

]


class DiffView(BaseDiffView):

    def diffs(self):
        diff = getToolByName(self.context, 'portal_diff')
        alldiffs = diff.createChangeSet(
            self.baseline,
            self.working_copy,
            id1="Baseline",
            id2="Working Copy")
        # import pdb; pdb.set_trace( )
        alldiffs._diffs = [
            di for di in alldiffs._diffs if di.field not in SKIP_FIELDS]
        return alldiffs
