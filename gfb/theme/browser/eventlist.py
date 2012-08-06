# -*- coding: utf-8 -*-
"""The List Events view."""

from datetime import date
from iwwb.eventlist import _
from iwwb.eventlist.interfaces import IIWWBSearcher
from iwwb.eventlist.interfaces import IListEventsForm
from iwwb.eventlist.interfaces import IWWB_SEARCHABLE_FIELDS
from iwwb.eventlist.browser.eventlist import ListEventsForm, ListEventsView
from plone.z3cform.layout import FormWrapper
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import logging

logger = logging.getLogger('iwwb.eventlist')


class GFBListEventsView(ListEventsView):
    """A BrowserView to display the ListEventsForm along with its results."""
    index = ViewPageTemplateFile('templates/eventlist.pt')
