import codecs
# import orjson
from io import BytesIO

import django_filters
# from django.contrib.gis.forms import PointField
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Count, Value, CharField
from django.http import HttpResponse
# from django.template.response import TemplateResponse
from django.utils import timezone
# from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
# from django.views.decorators.gzip import gzip_page
from django_filters.views import FilterView
# from djgeojson import GEOJSON_DEFAULT_SRID
# from djgeojson.http import HttpGeoJSONResponse
# from djgeojson.serializers import DjangoGeoJSONEncoder
# from djgeojson.views import GeoJSONResponseMixin
# from numpy import datetime64
from pandas.core.dtypes import dtypes

from djaesy.actions.forms import ConfirmActionForm
from djaesy.security.permission import get_permission
from djaesy.actions.views import Action
from djaesy.core.views.model import BaseModelView


class BaseListView(FilterView, BaseModelView):

    control_sidebar_icon = 'mdi mdi-magnify'
    control_sidebar_title = _('Filtros')

    _model_columns = []
    data_columns = []
    table_columns = []

    create_url_name = ''
    update_url_name = ''
    delete_enable = True

    filterset_class = None
    filterset = None

    related_link = {}

    export_columns = []
    export_formatters = {}

    filter_by = []
    declared_filters = []
    filter_defaults = []

    total_count = 0
    filtered_count = 0
    is_filtered = False

    default_actions = [
        Action(
            label=_('Remover'), action='delete_action', permission='delete',
            icon='mdi mdi-trash-can-outline', form=ConfirmActionForm, item=True
        ),
        Action(
            label=_('Excel'), action='export_to_excel_action', permission='export',
            icon='mdi mdi-file-excel', max_selected=-1
        ),
        Action(
            label=_('CSV'), action='export_to_csv_action', permission='export',
            icon='mdi mdi-file-document-outline', max_selected=-1
        )
    ]

    item_default_actions = [
        Action(
            label=_('Remover'), action='delete_action', permission='delete',
            icon='mdi mdi-trash-can-outline', form=ConfirmActionForm
        )
    ]

    default_actions_display = {
        'main_actions': ['delete_action'],
        'secondary_groups': [
            {
                'name': 'Exportar',
                'icon': 'mdi mdi-application-export',
                'actions': [
                    'export_to_excel_action',
                    'export_to_csv_action'
                ]
            }
        ],
        # 'actions_group': ['delete_action', 'export_to_excel_action', 'export_to_csv_action']
    }

    @property
    def model_columns(self):
        if not self._model_columns:
            table_columns = getattr(self, 'table_columns', [])
            data_columns = getattr(self, 'table_columns', [])
            model_columns = list(map(lambda f: f.attname, self.model._meta.fields))
            self._model_columns = data_columns or table_columns or data_columns or model_columns
        return self._model_columns

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        class Filter(django_filters.FilterSet):

            filter_defaults_ = self.filter_defaults

            def __init__(self, data, *args, **kwargs):
                data = data.copy() if data else {}
                for default_ in self.filter_defaults_:
                    assert isinstance(default_, tuple) and len(default_) == 2
                    key, value = default_
                    data.setdefault(key, value)
                super(django_filters.FilterSet, self).__init__(data, *args, **kwargs)

            class Meta:
                model = self.model
                fields = self.filter_by
                filter_overrides = {
                    # PointField: {
                    #     'filter_class': django_filters.CharFilter,
                    #     'extra': lambda f: {
                    #         'lookup_expr': 'dwithin',
                    #     },
                    # },
                }

        for field_filter in self.declared_filters:
            assert field_filter.field_name is not None
            Filter.base_filters[field_filter.field_name] = field_filter

        self.filterset_class = Filter


    def get_queryset(self):

        queryset = super().get_queryset()

        for column in self.model_columns:
            if '___' in column:
                action, column_data = column.split('___')
                if action == 'count':
                    queryset = queryset.annotate(**{column: Count(column_data, distinct=True)})
                elif action == 'dummy':
                    queryset = queryset.annotate(**{column: Value(None, output_field=CharField())})
                    if column not in self.table_formatters:
                        raise ImproperlyConfigured(f'Error on dummy column "{column_data}": missing table formatter.')

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)

        return self.filterset.qs.distinct()

    def get_context_data(self, *, object_list=None, filter=None, **kwargs):

        context = super().get_context_data(object_list=object_list, **kwargs)

        total_count = self.filterset.queryset.count()
        filtered_count = self.filterset.qs.count()
        is_filtered = bool(total_count != filtered_count)

        context.update({
            'filterset': self.filterset,
            'total_count': total_count,
            'filtered_count': filtered_count,
            'is_filtered': is_filtered,
            'has_control_sidebar': bool(total_count) and (self.filter_by or self.declared_filters),
            'footer': bool(total_count),
        })

        context.update(self._get_render_context(context))

        return context

    def _get_render_context(self, context={}):

        context = super()._get_render_context(context)
        user = self.request.user

        add, by_model = get_permission(permission_type='add', model=self.model)
        delete, by_model = get_permission(permission_type='delete', model=self.model) # permissions_by_model=by_model)
        change, by_model = get_permission(permission_type='change', model=self.model) # permissions_by_model=by_model)

        can_create = True if user.has_perm(add) and self.create_url_name else False
        can_change = True if user.has_perm(change) and self.update_url_name else False
        can_delete = True if user.has_perm(delete) and self.delete_enable else False

        has_actions = can_create or can_change or can_delete

        context.update({
            'create_url_name': self.create_url_name,
            'update_url_name': self.update_url_name,
            'can_create': can_create,
            'can_delete': can_delete,
            'can_change': can_change,
            'has_actions': has_actions
        })

        return context

    def get_export_dataframe(self, qs):
        export_columns = self.export_columns or self.model_columns
        df, columns, first_column, column_headers = self._get_dataframe(export_columns, qs)
        try:
            df = self._fix_df_empty_values(df)
        except:
            pass
        return df

    def get_export_file_name(self, extension):
        now = timezone.now()
        now = now.strftime("%Y%m%d_%H%M%S")
        vn = self._get_verbose_names()
        file_prefix = slugify(vn['verbose_name_plural'])
        return f'{file_prefix}_{now}.{extension}'

    @staticmethod
    def export_to_excel_action(qs, request, form=None, view=None):

        df = view.get_export_dataframe(qs)
        df = df.rename(columns={"pk": "ID"})

        # Remove timezone to export to excel
        c = 0
        for column_type in df.dtypes:
            if isinstance(column_type, dtypes.DatetimeTZDtype):
                df.iloc[:, c] = df.iloc[:, c].dt.tz_localize(None)
            c += 1

        xls_file = BytesIO()
        df.to_excel(xls_file, index=False, float_format="%.2f")
        size = xls_file.tell()
        xls_file.seek(0)

        file_name = view.get_export_file_name('xlsx')

        response = HttpResponse(
            xls_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        response['Content-Length'] = size

        return response

    @staticmethod
    def export_to_csv_action(qs, request, form=None, view=None):
        df = view.get_export_dataframe(qs)
        df = df.rename(columns={"pk": "ID"})

        csv_file = BytesIO()
        csv_file.write(codecs.BOM_UTF8)
        csv_file.write(df.to_csv(index=False).encode())
        size = csv_file.tell()
        csv_file.seek(0)

        file_name = view.get_export_file_name('csv')

        response = HttpResponse(csv_file, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        response['Content-Length'] = size

        return response