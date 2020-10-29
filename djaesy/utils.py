from importlib import import_module

from django.urls.base import resolve


def load_view(view_ref):
    view_app, view_class = view_ref.split('.')
    return getattr(import_module(f'{view_app}.views'), view_class)


def load_form(form_ref):
    form_app, form_class = form_ref.split('.')
    return getattr(import_module(f'{form_app}.forms'), form_class)


def get_view_from_url(url):
    """
    :param <str> url:
    :return: Instance of view
    """
    try:
        view_func = resolve(url).func
        view = view_func.view_class

        return view
    except Exception as e:
        raise Exception(f'djaesy.utils.get_view_from_url: {e}')
