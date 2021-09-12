import inspect

from dal import autocomplete
from django.urls import path


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
