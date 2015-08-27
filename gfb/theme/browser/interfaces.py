from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from zope.interface import Interface


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IGFBEditBelowcontenttitle(IViewletManager):
    """ ViewletManager for edit forms """


class IGFB(Interface):
    """ A tool view with GFB specifics """

    def cropHTMLText(text, length, ellipsis):
        """ First strip HTML, then crop on a word boundary """

    def mail_wf_change(state_change, **kwargs):
        """ send email """

    def show_submit_action(obj):
        """ whether to show the WF tab 'Submit' """

    def show_checkout_action(obj):
        """ whether to show the action Tab 'Create Working Copy'"""


class IHomeFolder(Interface):
    """ Marker Interface for a home folder """


class IDiffView(Interface):
    """ Marker interface for our custom diff view """