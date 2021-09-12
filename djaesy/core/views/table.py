# import orjson

import pandas
# from django.contrib.gis.forms import PointField
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import InvalidPage
from django.db.models import QuerySet
from django.http import Http404
# from django.template.response import TemplateResponse
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _


# from django.views.decorators.gzip import gzip_page
# from djgeojson import GEOJSON_DEFAULT_SRID
# from djgeojson.http import HttpGeoJSONResponse
# from djgeojson.serializers import DjangoGeoJSONEncoder
# from djgeojson.views import GeoJSONResponseMixin
# from numpy import datetime64
from djaesy.core.views.list import BaseListView


class TableListView(BaseListView):

    model = None
    template_name = 'djaesy/crud/list.html'

    delete_enable = True
    select_column = True

    table_columns = []
    table_column_headers = {}
    table_formatters = {}
    hidden_columns = []

    has_control_sidebar = True
    control_sidebar_open = True
    control_sidebar_toggle = True
    option_footer = True

    paginate_by = 50
    page_sizes = [10, 20, 30, 50, 100]

    @staticmethod
    def get_page_range(page, show_size, total):

        if page > total:
            page = total
        elif page < 1:
            page = 1

        if not show_size % 2 == 1:
            show_size = int(show_size) + 1

        if total <= show_size:
            return range(1, total + 1)

        middle = int(show_size / 2)
        left_limit = middle
        right_limit = total - middle

        if page <= left_limit:
            return range(1, show_size + 1)
        elif page >= right_limit:
            return range(total - show_size + 1, total + 1)
        else:
            left = page - middle
            right = page + middle
            return range(left, right + 1)

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            page_number = 1
        try:
            page = paginator.page(page_number)
            return paginator, page, page.object_list, page.has_other_pages()
        except InvalidPage as e:
            page = paginator.page(1)
            return paginator, page, page.object_list, page.has_other_pages()

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(object_list=object_list, **kwargs)

        context['list_table'] = self.build_table(context['object_list'])

        context['page_sizes'] = self.page_sizes
        if context['is_paginated']:
            context['paginator_range'] = self.get_page_range(
                context['page_obj'].number, 5, context['paginator'].num_pages
            )
            context['page_size'] = context['paginator'].per_page
        else:
            context['page_size'] = int(self.request.GET.get('page_size', 0)) or self.paginate_by

        # context.update(self._get_render_context(context)) # 2

        return context

    def _get_table_headers(self, table_columns):

        column_headers = []

        for column in table_columns:
            if column in self.table_column_headers:
                column_headers.append(self.table_column_headers[column])
            else:
                if '___' in column:
                    column_headers.append(column)
                else:
                    if '__' in column:
                        column = column.split('__')[0]
                    column_headers.append(getattr(self.model, column).field.verbose_name.capitalize())

        first_column = column_headers[0]
        column_headers = ['pk'] + column_headers

        columns = ['pk'] + self.table_columns

        return columns, first_column, column_headers

    def _get_dataframe(self, df_columns, qs):
        qs = self.object_list if not qs else qs
        columns, first_column, column_headers = self._get_table_headers(df_columns)
        column_headers = [str(col) for col in column_headers]
        df = pandas.DataFrame(qs.values_list(*columns), columns=column_headers)
        return df, columns, first_column, column_headers

    def _fix_df_empty_values(self, df):
        mask = df.applymap(lambda x: x is None)
        cols = df.columns[(mask).any()]
        for col in df[cols]:
            df.loc[mask[col], col] = '-'
        return df

    def get_records(self, qs, columns):
        records = list(map(list, list(qs.values_list(*columns))))
        return records

    def build_table(self, queryset):

        assert isinstance(queryset, QuerySet)
        assert len(self.table_columns) > 0

        columns, first_column, column_headers = self._get_table_headers(self.table_columns)
        df = self.get_records(queryset, columns)

        if self.table_formatters:
            for column, formatter in self.table_formatters.items():
                assert callable(formatter)
                column_id = columns.index(column)
                for row in df:
                    try:
                        named_row = dict(zip(columns,  row))
                        row[column_id] = formatter(row[column_id], named_row, column, self.request)
                    except TypeError as e:
                        raise ImproperlyConfigured(f'Error on formatter "{formatter.__name__}". The formatter function must implement the following arguments: [column_value, row, column, request]')

        related_links = {}
        for related_column, data in self.related_link.items():
            column_idx = columns.index(related_column)
            link_url = reverse_lazy(data['url'])
            link_value_idx = columns.index(data['filter_value'])
            related_links[column_idx + 1] = {
                'url': f'{link_url}?{data["filter"]}=',
                'value': link_value_idx,
                'link_text': data.get('link_text', '<i class="mdi mdi-arrow-top-right"></i>')
            }

        default_order = None
        if self.ordering:
            if '-' in self.ordering:
                order_key = str(self.ordering).replace('-', '')
                default_order = 'desc'
            else:
                order_key = self.ordering
                default_order = 'asc'

        default_order_by = self.table_columns.index(order_key)+1 if self.ordering else 0

        order_by = int(self.request.GET.get('order_by', default_order_by))
        order = self.request.GET.get('order', default_order)

        hidden_indexes = list(map(lambda col: columns.index(col), self.hidden_columns))

        unsortable_columns = filter(lambda col: col.startswith('dummy___'), columns)
        unsortable_columns_indexes = list(map(lambda col: columns.index(col), unsortable_columns))

        return {
            'table': df,
            'update_url': self.update_url_name,
            'table_id': 'list_datatable',
            'table_classes': 'dataframe datatable table table-sm table-hover mb-0 list_view_table',
            'table_headers': column_headers,
            'hidden_columns': hidden_indexes,
            'unsortable_columns': unsortable_columns_indexes,
            'related_links': related_links,
            'order': order,
            'order_by': column_headers[order_by] if order_by else None,
            'select_column': self.select_column
        }

    def _process_get(self):

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })

    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get('page_size', None)
        if not page_size:
            return self.paginate_by
        else:
            try:
                return min(self.page_sizes, key=lambda x: abs(x - int(page_size)))
            except:
                return self.paginate_by

    def get_ordering(self):

        order_by = self.request.GET.get('order_by', None)
        order = self.request.GET.get('order', None)

        if order_by and order:
            order_by = int(order_by)
            if order_by <= 0:
                return self.ordering
            else:
                order_by = order_by - 1
                order_by = self.table_columns[order_by]

            if order == 'desc':
                order_by = f'-{order_by}'

            return order_by

        return self.ordering

    def post(self, request):
        # permission, permissions_by_model = get_permission(permission_type='add', model=self.model)
        #
        # if not permission or request.user.has_perm(permission):
        self._process_get()
        return self._handle_action_post(request)

    def get(self, request, *args, **kwargs):
        self._process_get()
        context = self.get_context_data()
        return self.render_to_response(context)
