from iwwb.eventlist.browser.eventlist import ListEventsView, ListEventsForm
from plone.z3cform.templates import subform_factory
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser.pagetemplatefile import BoundPageTemplate
from Products.CMFCore.utils import getToolByName


class GFBListEventsForm(ListEventsForm):

    def update(self):
        super(GFBListEventsForm, self).update()
        # We define the <form> tag manually, therefore we use the subform
        # as template here
        template = subform_factory(self, self.request)
        self.template = BoundPageTemplate(template, self)


class GFBListEventsView(ListEventsView):
    """A BrowserView to display the ListEventsForm along with its results."""
    index = ViewPageTemplateFile('templates/eventlist.pt')
    form = GFBListEventsForm

    def get_preselection(self):
        tool = getToolByName(self.context, 'portal_vocabularies')
        vocab_name = 'eventlist_preselection'
        if vocab_name not in tool:
            return list()
        vocab_dict = tool[vocab_name].getVocabularyDict(
            self.context)
        return [x[0] for x in vocab_dict.values()]
