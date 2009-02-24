## Controller Validator "validate_captcha"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=captcha_text='', captcha_id=''
##title=validates the Registration of a User
##
ch = context.restrictedTraverse('/@@captcha_helper')

res = ch.verifyCaptcha(context)
if res:
    state.setError('captcha_text', res)

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors. (%s)' % res)
else:
    return state.set(status='success')
