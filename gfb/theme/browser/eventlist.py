from iwwb.eventlist.browser.eventlist import ListEventsView, ListEventsForm
from plone.z3cform.templates import subform_factory
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser.pagetemplatefile import BoundPageTemplate


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
