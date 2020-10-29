import inspect

from dal import autocomplete
from dal_select2.widgets import ListSelect2 as DALListSelect2
from dal_select2.widgets import ModelSelect2 as DALModelSelect2
from dal_select2.widgets import ModelSelect2Multiple as DALModelSelect2Multiple
from dal_select2.widgets import Select2 as DALSelect2, I18N_PATH
from dal_select2.widgets import Select2Multiple as DALSelect2Multiple
from dal_select2.widgets import TagSelect2 as DALTagSelect2
from django.forms import forms
from django.urls import path


def _media(self):
    """Return JS/CSS resources for the widget."""
    i18n_name = self._get_language_code()
    i18n_file = (
        '%s%s.js' % (I18N_PATH, i18n_name),
    ) if i18n_name else ()

    return forms.Media(
        js=i18n_file + (
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/jquery.post-setup.js',
        ),
    )


class Select2(DALSelect2):
    @property
    def media(self):
        return _media(self)


class Select2Multiple(DALSelect2Multiple):
    @property
    def media(self):
        return _media(self)


class ListSelect2(DALListSelect2):
    @property
    def media(self):
        return _media(self)


class ModelSelect2(DALModelSelect2):
    @property
    def media(self):
        return _media(self)


class ModelSelect2Multiple(DALModelSelect2Multiple):
    @property
    def media(self):
        return _media(self)


class TagSelect2(DALTagSelect2):
    @property
    def media(self):
        return _media(self)


class AutocompleteCombo:
    autocompletes = []

    def __init__(self):

        methods = inspect.getmembers(self, predicate=inspect.isfunction)

        for name, function in methods:
            if not name.startswith('_'):
                ac_function = type(f'{name.title()}Autocomplete', (autocomplete.Select2QuerySetView,), {
                    'get_queryset': function,
                })
                self.autocompletes.append((name, ac_function))

    @property
    def urls(self):

        paths = []

        for name, ac in self.autocompletes:
            paths.append(path(f'{name}/autocomplete', ac.as_view(), name=f'{name}_autocomplete'))

        return paths

    @staticmethod
    def _basic(self, model):

        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return model.objects.none()

        qs = model.objects.all()

        # company = self.forwarded.get('company', None)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

    @staticmethod
    def _visible(self, model, qs=None, filter_field='name'):

        if qs is None:
            if not self.request.user.is_authenticated:
                return model.objects.none()
            qs = model.visible.all()

        relationship = self.forwarded.get('relationship', None)
        company = self.forwarded.get('company', None)
        representative = self.forwarded.get('representative', None)
        client = self.forwarded.get('client', None)

        if relationship is not None:
            relationship = int(relationship)
            if relationship == 0:
                qs = qs.filter(relationship=0)
            elif company and relationship == 1:
                qs = qs.filter(company_id=int(company))
            elif representative and relationship == 2:
                qs = qs.filter(representative_id=int(representative))
            elif client and relationship == 3:
                qs = qs.filter(client_id=int(client))
            else:
                qs = qs.none()

        if self.q:
            qs = qs.filter(**{f'{filter_field}__icontains': self.q})

        return qs

    @classmethod
    def get_forwards(cls, self):
        for field, value in self.forwarded.copy().items():
            if isinstance(value, list):
                self.forwarded[field] = [int(i) for i in value]
        return self.forwarded
