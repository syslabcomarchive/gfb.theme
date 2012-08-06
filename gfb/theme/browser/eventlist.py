# -*- coding: utf-8 -*-
"""The List Events view."""

from iwwb.eventlist.browser.eventlist import ListEventsView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class GFBListEventsView(ListEventsView):
    """A BrowserView to display the ListEventsForm along with its results."""
    index = ViewPageTemplateFile('templates/eventlist.pt')
