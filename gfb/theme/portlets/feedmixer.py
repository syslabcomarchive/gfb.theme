from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.feedmixer.portlet import Renderer as base

class Renderer(base):
    """Portlet renderer.
    """
    render = ViewPageTemplateFile("feedmixer.pt")
