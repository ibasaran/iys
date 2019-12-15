from django.shortcuts import redirect
from django.conf import settings
from re import compile
from django.http import HttpResponseRedirect


EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.open_urls = [self.login_url] + \
                         getattr(settings, 'OPEN_URLS', ['/admin/'])

    def __call__(self, request):
        response = self.get_response(request)
        if (not request.user.is_authenticated):
            if (not request.path_info in self.open_urls):
                print('GİRDDİİİİ')
                return redirect(self.login_url+'?next='+request.path)

        return response

#    def __call__(self, request):
#        if not request.user.is_authenticated:
#            path = request.path_info.lstrip('/')
#            if not any(m.match(path) for m in EXEMPT_URLS):
#                return HttpResponseRedirect(settings.LOGIN_URL)
