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

    def _construct_query(self):
        """Parse the searchable fields from the form."""
        querydict = {}

        for field in IWWB_SEARCHABLE_FIELDS:
            if field == 'query':
                value = self.request.get('form.widgets.query')
                if not value:
                    continue
                words = value.split()
                search_all_words = self.request.get('form.widgets.allWords')
                if search_all_words:
                    querydict[field] = u" AND ".join(words)
                else:
                    # If no operator is specified it searches for all the
                    # words (XXX: OR operator doesn't work as expected?)
                    querydict[field] = words
            elif field == 'startMonth':
                year = self.request.form.get('form.widgets.%s-year' % field)
                month = self.request.form.get('form.widgets.%s-month' % field)
                day = '1'
                if year and month:
                    event_date = date(int(year), int(month), int(day))
                    querydict['startDate'] = event_date.isoformat()
            elif field == 'zipcity':
                value = self.request.get('form.widgets.%s' % field)
                if not value:
                    continue
                if ',' in value:
                    zips = [x.strip() for x in value.split(',')
                        if x.strip().isdigit()]
                    if len(zips) > 0:
                        querydict['zip'] = value
                elif value.strip().isdigit():
                    querydict['zip'] = int(value)
                else:
                    querydict['city'] = value
            else:
                value = self.request.get('form.widgets.%s' % field)
                if not value:
                    continue
                # Some field values are lists, convert them to string
                if isinstance(value, (list, tuple)):
                    value = ','.join(value)
                querydict[field] = value

        termine = self.request.get('form.widgets.startTimeRequired')
        if termine:
            querydict['termine'] = 'yes'
        return querydict
