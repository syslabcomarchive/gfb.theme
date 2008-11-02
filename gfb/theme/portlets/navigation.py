from plone.app.portlets.portlets import navigation

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Renderer(navigation.Renderer):
    """Dynamically override standard header for navtree portlet"""
    
    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('navigation_recurse.pt')