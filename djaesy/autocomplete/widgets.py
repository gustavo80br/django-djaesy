from dal_select2.widgets import ListSelect2 as DALListSelect2
from dal_select2.widgets import ModelSelect2 as DALModelSelect2
from dal_select2.widgets import ModelSelect2Multiple as DALModelSelect2Multiple
from dal_select2.widgets import Select2 as DALSelect2, I18N_PATH
from dal_select2.widgets import Select2Multiple as DALSelect2Multiple
from dal_select2.widgets import TagSelect2 as DALTagSelect2
from django.forms import forms


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
