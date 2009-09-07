import settings
import logging

def context_processor(request):
    '''
    Add a 'MOBILE' context variable if the user agent is detected as being
    a mobile browser.
    '''
    context = {}
    if is_mobile(request):
        context["MOBILE"] = True
    context["BASE_URL"] = request.build_absolute_uri("/")[0:-1]
    return context

def is_mobile(request):
    '''
    True if user agent is detected as a mobile browser
    '''
    browser = request.META['HTTP_USER_AGENT']
    if browser.find('MIDP') >= 0 or browser.find('OPWV') == 0:
        return True
    else:
        return False