# utils.py
from re import compile
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
login_not_required_urls = [compile(expr) for expr in getattr(settings, 'LOGIN_NOT_REQUIRED_URLS', [])]
allowed_tenant_areas = [compile(expr) for expr in getattr(settings, 'ALLOWED_TENANT_AREA', [])]
allowed_employee_areas = [compile(expr) for expr in getattr(settings, 'ALLOWED_EMPLOYEE_AREA', [])]


class LoginRequiredMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        # return redirect('/website/hello')
        if not request.user.is_authenticated:
            print("------Not authentucated")
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in login_not_required_urls):
                return redirect('{}?next={}'.format(settings.LOGIN_URL, request.path))
     

        else:
            if request.user.is_tenant:
                print("------Not ssss")
                path = request.path_info.lstrip('/')
                if not any(m.match(path) for m in login_not_required_urls):
                    if not any(m.match(path) for m in allowed_tenant_areas):
                        return redirect('/accounts/logout/')
            if request.user.is_employee:
                print("------Not sss444444ss")
                path = request.path_info.lstrip('/')
             
                if not any(m.match(path) for m in login_not_required_urls):
                    if not request.user.is_paid:
                        return redirect('/paybill/make_payment/')
                    if not any(m.match(path) for m in allowed_employee_areas):
                        return redirect('/property/')