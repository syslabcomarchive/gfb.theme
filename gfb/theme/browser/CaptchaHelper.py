# -*- coding: utf-8 -*-
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from Products.CMFPlone import utils
from Products.Five import BrowserView
from collective.captcha.browser.captcha import Captcha, COOKIE_ID


class ICaptchaHelper(Interface):
    """ This interface holds utility methods for using collective.captcha
    """

    def createCaptcha(context, request):
        """ Use context and request to create and return a Captcha object """

    def verifyCaptcha(context):
        """ Validate the user's input for a given captcha """


class CaptchaHelper(BrowserView):
    implements(ICaptchaHelper)

    def createCaptcha(self, context, request=None):
        """ See interface """
        if not request:
            request = context.REQUEST
        request[COOKIE_ID] = ''     #, '6552fec8867ee2a85a44784dda007e49efcf50ef')
        captcha = Captcha(context, request)
        return captcha


    def verifyCaptcha(self, context, request=None):
        """ See interface """
        verify_failed_msg = "You need to enter the code shown to verify your request"
        if not request:
            request = context.REQUEST
        if not COOKIE_ID in request.cookies:
            return "No Captcha cookie was found"
        text = request.get('captcha_text', None)
        if not text:
            return verify_failed_msg
        captcha =Captcha(context, request)
        if not captcha.verify(text):
            return verify_failed_msg
        return ""