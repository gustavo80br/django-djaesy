from django.shortcuts import redirect
from django.urls import resolve

from djaesy.views import DjaesyTabViewWrapper


class ChangePassword:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user = request.user
        if getattr(user, 'must_change_password', False):
            url_name = resolve(request.path_info).url_name
            if not url_name == 'user_change_password' and not url_name == 'logout':
                return redirect('user_change_password')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class UrlRouter:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        if request.method == 'GET' and request.headers.get('Sec-Fetch-Dest', '') != 'iframe':
            view_class = getattr(view_func, 'view_class', None)
            if view_class:
                use_tabs = getattr(view_class, 'option_use_tabs', True)
                if use_tabs:
                    url_path = [request.META["PATH_INFO"]]
                    if request.META["QUERY_STRING"]:
                        url_path.append(request.META["QUERY_STRING"])
                    raw_url = '?'.join(url_path)
                    return DjaesyTabViewWrapper.as_view()(request, raw_url=raw_url)

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
