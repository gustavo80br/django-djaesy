from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.utils import translation
from django.views.generic.base import View


class SetLanguage(View):

    def get(self, request, language):

        if language not in dict(settings.LANGUAGES).keys():
            user_language = 'pt-br'
        else:
            user_language = language

        translation.activate(user_language)

        response = HttpResponseRedirect('/')
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)

        return response
