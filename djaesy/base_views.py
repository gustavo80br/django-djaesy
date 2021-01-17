# -*- coding: utf-8 -*-

# CHECK THIS OUT: https://ccbv.co.uk/

import codecs
import json
# import orjson
from io import BytesIO

import django_filters
import pandas
from crispy_forms.helper import FormHelper
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
# from django.contrib.gis.forms import PointField
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import InvalidPage
from django.db.models import QuerySet, Count, Value, CharField
from django.db.models.deletion import ProtectedError
from django.forms import models as model_forms
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
# from django.template.response import TemplateResponse
from django.urls import reverse_lazy, path
from django.utils import timezone
# from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.views import View
# from django.views.decorators.gzip import gzip_page
from django.views.generic import CreateView as DjangoCreateView
from django.views.generic import DetailView as DjangoDetailView
from django.views.generic import FormView as DjangoFormView
from django.views.generic import UpdateView as DjangoUpdateView
from django_filters.views import FilterView
# from djgeojson import GEOJSON_DEFAULT_SRID
# from djgeojson.http import HttpGeoJSONResponse
# from djgeojson.serializers import DjangoGeoJSONEncoder
# from djgeojson.views import GeoJSONResponseMixin
# from numpy import datetime64
from pandas.core.dtypes import dtypes

from djaesy.autocomplete import ModelSelect2, ModelSelect2Multiple
from djaesy.forms import ConfirmActionForm, BaseActionForm
from djaesy.menu import Menu, MenuItem
from djaesy.permission import get_permission

# from silk.profiling.profiler import silk_profile


# https://django-leaflet.readthedocs.io/en/latest/templates.html#use-leaflet-api
# https://cloud.maptiler.com/ (google account gustavo@fundacaoaprender.org.br)
# https://www.arcgis.com/home/webmap/viewer.html

# TODO: Individualizar Geo funcoes'
MAP_SETTINGS = {
    'SRID': 4326,
    'TILES': [
        (
            'Mapa',
            'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
            {
              'attribution': 'CARTO DB',
              'maxZoom': 22
            }
        ),
        (
            'Satelite',
            'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            {
                'attribution': 'ArcGIS Online',
                'maxZoom': 17
            }
        ),
        (
            'Relevo',
            'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
            {
                'attribution': 'ArcGIS Online',
                'maxZoom': 18
            }
        ),
    ],
    'ATTRIBUTION_PREFIX': '<a href="https://i3track.com.br">i3Track ®</a>',
    'DEFAULT_CENTER': (-22.2864684, -45.8961274),
    'DEFAULT_ZOOM': 3,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 22,
}


class Action:

    def __init__(
            self, label, action, permission=None, max_selected=0, icon=None, form=None, modal_title=None, modal_text=None, item=False):

        self.action = None
        self.form = None
        self.form_instance = None
        self.permission = permission

        custom_form = False
        form_instance = None

        if not callable(action) and not isinstance(action, str):
            raise ImproperlyConfigured(
                'Action must be a callable or string of the method name'
            )
        if not isinstance(max_selected, int):
            raise ImproperlyConfigured(
                'Max Selection options are: -1: no selection needed. 0: one or more, N: max N items selected'
            )

        if form:
            if not issubclass(form, BaseActionForm):
                raise ImproperlyConfigured('Action Form must be extended from BaseActionForm.')
            custom_form = True
        else:
            form = BaseActionForm

        self._args_list = []
        local_vars = locals().copy().items()
        for arg, value in local_vars:
            if not arg == 'self':
                setattr(self, arg, value)
                self._args_list.append(arg)

    def set_view(self, view_obj, action_id):
        if isinstance(self.action, str):
            self.action = getattr(view_obj, self.action)

        self.form_instance = self.form(initial={'action_form': action_id})

    def as_dict(self, action_id):
        as_dict = {'id': action_id}
        for arg in self._args_list:
            as_dict[arg] = getattr(self, arg)
        as_dict['action_name'] = as_dict['action'].__name__
        return as_dict

    def has_permission(self, user, permission_model):
        try:
            permission, permissions_by_model = get_permission(permission_type=self.permission, model=permission_model)
            if not permission or user.has_perm(permission):
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f'Action.has_permission: {e}')


# BASE VIEWS

class BaseView(View):

    page_title = ''
    content_title = ''
    back_url_name = ''
    icon = ''

    template_name = 'djaesy/base.html'

    # Layout Options
    # --------------

    # View in tab
    option_open_in_tabs = True

    # Navbar
    option_navbar_logo = True

    # Layout
    option_fluid_layout = True
    option_sm_layout_size = 12
    option_md_layout_size = 12
    option_lg_layout_size = 12
    option_xl_layout_size = 12

    # Sidebar
    option_menubar_open = False
    option_menubar_toggle = True

    # Simplebar scroller
    option_simplebar_scroller = True

    # Fullscreen
    option_in_fullscreen = False
    option_fullscreen_toggle = True

    # Footer
    option_footer = False

    # Control sidebar
    option_sidebar = True
    option_sidebar_open = False
    option_sidebar_toggle = True
    option_sidebar_title = ''
    option_sidebar_icon = 'mdi mdi-filter-variant'
    option_sidebar_size = '240px'
    option_sidebar_color = ''

    # Control sidebar as help area
    option_side_help_title = _('Saiba mais')
    option_side_help_icon = 'mdi mdi-comment-question-outline'
    option_side_help = ''

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self._get_render_context())

    def _get_render_context(self, context=None):

        if not context:
            context = {}

        body_class, options = self._build_options()

        context.update(self._get_titles())

        context.update({
            'options': options,
            'body_class': body_class,
            'back_url_name': self.back_url_name,
            'control_sidebar_icon': self.option_sidebar_icon,
            'control_sidebar_title': self.option_sidebar_title,
        })

        context.update(self._get_icons())
        context.update(self._side_help())

        return context

    def _get_icons(self):
        icons = {}
        if self.icon:
            icons['page_icon'] = self.icon
        return icons

    def _get_titles(self):
        titles = {}
        titles['page_title'] = 'AppPanel BaseView page_title attribute' if not str(self.page_title) else str(self.page_title)
        titles['content_title'] = 'AppPanel BaseView content_title attribute' if not str(self.content_title) else str(self.content_title)
        titles['full_page_title'] = ' | '.join((str(settings.APPLICATION_PAGE_TITLE_PREFIX), titles.get('page_title', '')))

        return titles

    def _get_options(self):
        options = {}
        for attr in dir(self):
            if attr.startswith('option_'):
                attr_key = attr.replace('option_', '')
                options[attr_key] = getattr(self, attr)
        return options

    def _build_options(self):

        options = self._get_options()

        body_class = ['fixed', 'control-sidebar-push-content', 'sidebar-push-content']

        if options.get('footer', False):
            body_class.append('footer-on')

        sidebar = 'sidebar-open' if options.get('menubar_open', False) else 'sidebar-collapse sidebar-toggle'
        body_class.append(sidebar)

        if options.get('sidebar_open', False):
            body_class.append('control-sidebar-open')

        return ' '.join(body_class), options

    def _side_help(self):
        return {
            'side_help': self.option_side_help,
            'side_help_title': self.option_side_help_title,
            'side_help_icon': self.option_side_help_icon
        }


class BaseModelView(BaseView):

    model = None
    verbose_name = ''
    verbose_name_plural = ''
    action_title = ''

    _actions = []

    default_actions = [
        Action(
            label=_('Remover'), action='delete_action', permission='delete',
            icon='mdi mdi-trash-can-outline', form=ConfirmActionForm, item=True
        )
    ]

    actions = []
    default_actions_display = {
        'main_actions': [],
        'secondary_groups': [],
        'actions_group': []
    }

    actions_display = {}

    def _get_titles(self):
        titles = {}
        vn = self._get_verbose_names()
        action = self.action_title
        titles['page_title'] = f'{action} {vn["verbose_name"]}' if not str(self.page_title) else str(self.page_title)
        titles['content_title'] = f'{action} {vn["verbose_name"]}' if not str(self.content_title) else str(self.content_title)
        titles['full_page_title'] = ' | '.join((str(settings.APPLICATION_PAGE_TITLE_PREFIX), titles.get('page_title', '')))

        return titles

    def _get_render_context(self, context={}):
        base_context = super()._get_render_context(context)
        base_context.update(self._get_verbose_names())
        base_context.update(self._get_titles())

        if not self.request.POST:
            self._actions = []

        base_context['actions'] = self._setup_actions()

        return base_context

    def _get_verbose_names(self):
        verbose_names = {}
        try:
            model = getattr(self, 'model')
            if model:
                verbose_names['verbose_name'] = model._meta.verbose_name.title()
                verbose_names['verbose_name_plural'] = model._meta.verbose_name_plural.title()
        finally:
            return verbose_names

    def _setup_actions(self):
        try:

            if self._actions:
                return self._actions

            actions = self.default_actions + self.actions
            flat_actions = {}
            actions_list = []

            action_id = 0

            for action in actions:
                if not isinstance(action, str) and action.has_permission(self.request.user, self.model):
                    action_id += 1
                    action.set_view(self, action_id)
                    action_dict = action.as_dict(action_id)
                    actions_list.append(action_dict)
                    flat_actions[action_dict['action_name']] = action_dict
                    flat_actions[f'{action_dict["action_name"]}_instance'] = action

            action_display = self.default_actions_display.copy()

            self._actions = {
                'main_actions': [],
                'secondary_groups': [],
                'actions_group': [],
            }

            for group, actions in action_display.items():
                action_display[group] += self.actions_display.get(group, [])

                for action in action_display[group]:
                    if group != 'secondary_groups':
                        if action in flat_actions:
                            if flat_actions[f'{action}_instance'].has_permission(self.request.user, self.model):
                                self._actions[group].append(flat_actions[action])
                    else:
                        action_group = {'name': action['name'], 'icon': action['icon'], 'actions': []}

                        for action_in_group in action['actions']:
                            if action_in_group in flat_actions:
                                if flat_actions[f'{action_in_group}_instance'].has_permission(self.request.user, self.model):
                                    action_group['actions'].append(flat_actions[action_in_group])

                        if action_group['actions']:
                            self._actions[group].append(action_group)

            self._actions['actions_list'] = actions_list

            return self._actions
        except Exception as e:
            raise Exception(f'BaseModelView._setup_actions: {e}')

    def _run_action(self, action_id, qs, request, form=None):
        _actions = self._setup_actions()['actions_list']
        action = _actions[action_id-1]
        return action['action'](qs, request, form, self)

    def _handle_action_post(self, request):
        try:
            action_id = int(request.POST['action_form'])
            action = self._setup_actions()['actions_list'][action_id-1]

            self.object_list = self.get_queryset()

            permission, by_model = get_permission(permission_type=action['permission'], model=self.model)
            if request.user.has_perm(permission):
                selected = []
                if request.POST.get('selected_items', None):
                    selected = request.POST['selected_items'].split(',')
                    selected = list(map(lambda x: int(x), selected))

                form_class = action['form']
                action_invalid = False

                if form_class:
                    form = form_class(request.POST)
                else:
                    form = BaseActionForm(request.POST)

                if not form.is_valid():
                    self._actions[action_id-1]['form_instance'] = form
                    action_invalid = True
                else:
                    qs = self.model.objects.filter(pk__in=selected)
                    try:
                        response = self._run_action(action_id, qs, request)
                        if response:
                            return response
                        else:
                            messages.add_message(
                                request, messages.SUCCESS, _('Ação executada com sucesso.'), extra_tags='success'
                            )
                    except:
                        messages.add_message(
                            request,
                            messages.ERROR,
                            _('Erro na execução da ação. Entre em contao to com o admistrador do sistema.'),
                            extra_tags='error'
                        )

                context = self.get_context_data()
                if action_invalid:
                    context['action_invalid'] = action_id
                if selected:
                    context['previous_selected'] = ','.join(map(str, selected))
            else:
                context = {}
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(f'Sem permissão: {action["permission"]}.'),
                    extra_tags='error'
                )

            return render(request, self.template_name, context)
        except Exception as e:
            raise Exception(f'BaseModelView._handle_action_post: {e}')

    def post(self, request):
        return self._handle_action_post(request)

    @staticmethod
    def delete_action(qs, request, form=None, view=None):
        try:
            qs.delete()
        except ProtectedError as e:
            messages.add_message(request, messages.ERROR, _('Não foi possível por PROTECT.'), extra_tags='error')


class BaseFormModelView(BaseModelView):

    use_col_class = True
    form_col_xs = 12
    form_col_sm = 6
    form_col_md = 4
    form_col_lg = 3

    form_helper = None
    form_layout = None
    fields = None
    form_class = None

    list_url_name = ''

    widgets = {}
    form_rules = {}

    cascade_clear = {}
    cascade_disable = {}
    cascade_hide = {}

    object = None

    def _setup_form_rules(self):

        widgets = self.widgets or {}
        cascade_disable = {}
        cascade_clear = {}
        cascade_hide = {}

        form_rules = self.form_rules.copy()
        form_class_rules = getattr(self.form_class, 'form_rules', {})
        if callable(form_class_rules):
            form_class_rules = form_class_rules() or {}

        form_rules.update(form_class_rules)

        for field, ac in form_rules.items():

            is_dict = isinstance(ac, dict)
            is_string = isinstance(ac, str)

            url = ''
            attrs = {}
            forward = []
            disable = {}
            hide = {}

            if not is_string and not is_dict:
                raise ImproperlyConfigured(
                    'Form Rules must be a dictionary {type:[AUTOCOMPLETE_M2K | AUTOCOMPLETE_FK], url:"", attrs:{}, '
                    'forward:[], disable:{}} or string [AUTOCOMPLETE M2K| AUTOCOMPLETE_FK | NONE]'
                )
            elif is_string:
                ac_type = ac
            else:
                if not 'type' in ac:
                    raise ImproperlyConfigured('Autocompletes as dict must have a "type" key with values "M2M" or "FK"')
                else:
                    ac_type = ac['type']
                    url = ac.get('url', '')
                    attrs = ac.get('attrs', {})
                    forward = ac.get('forward', [])
                    disable = ac.get('disable', {})
                    hide = ac.get('hide', {})

            if ac_type == 'FK':
                ac_call = ModelSelect2
                attrs['class'] = ' pmd-select2 '
            elif ac_type == 'M2M':
                ac_call = ModelSelect2Multiple
                attrs['class'] = ' pmd-select2 '
            elif ac_type == 'NONE':
                ac_call = None
            else:
                raise ImproperlyConfigured('Autocompletes as string must be "M2M" or "FK"')

            if ac_call:
                ac_arguments = {
                    'url': url or f'{field}_autocomplete',
                    'attrs': attrs,
                    'forward': forward
                }
                widgets[field] = ac_call(**ac_arguments)

            if disable:
                cascade_disable[field] = disable

            if forward:
                cascade_clear[field] = forward

            if hide:
                cascade_hide[field] = hide

        return widgets, cascade_disable, cascade_clear, cascade_hide

    def _setup_helper(self, form_class=None):

        if self.form_helper:
            helper = self.form_helper
        else:
            helper = FormHelper()
            helper.form_show_labels = True
            helper.form_tag = False
            helper.include_media = False
            helper.form_show_errors = True
            if self.form_layout:
                helper.layout = self.form_layout
            elif self.use_col_class:
                helper.col_class = f'col col-{self.form_col_xs} col-sm-{self.form_col_sm} col-md-{self.form_col_md} ' \
                                   f'col-lg-{self.form_col_lg}'

        self.form_helper = helper

        return form_class

    def _get_form_class(self, form_class=None):

        widgets, cascade_disable, cascade_clear, cascade_hide = self._setup_form_rules()

        self._setup_helper()

        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:

            widgets_dict = widgets
            form_widgets = getattr(self.form_class._meta, 'widgets', {}) or {}
            widgets_dict.update(form_widgets)

            class FormClass(self.form_class):
                class Meta(self.form_class.Meta):
                    widgets = widgets_dict

            self.form_class = FormClass
            return self.form_class
        else:
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif getattr(self, 'object', None) is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
                model = self.get_queryset().model

            if self.fields is None:
                form_class = model_forms.modelform_factory(model, exclude=[], widgets=widgets)
            else:
                form_class = model_forms.modelform_factory(model, fields=self.fields, widgets=widgets)

            return form_class

    def _get_render_context(self, context={}):

        context = super()._get_render_context(context)

        context['list_url_name'] = self.list_url_name
        context['form_helper'] = self.form_helper

        widgets, cascade_disable, cascade_clear, cascade_hide = self._setup_form_rules()

        context['cascade_clear'] = json.dumps(cascade_clear)
        context['cascade_disable'] = json.dumps(cascade_disable)
        context['cascade_hide'] = json.dumps(cascade_hide)

        form = context.get('form', None)
        if form:
            if form.errors:
                for field, error in form.errors.items():
                    title = f'<h6 class="toast-message"><strong>{str(field).capitalize()}</strong></h6>'
                    msg = '<br/>'.join(error)
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        mark_safe(title + msg),
                        extra_tags='error'
                    )

        return context


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
                    PointField: {
                        'filter_class': django_filters.CharFilter,
                        'extra': lambda f: {
                            'lookup_expr': 'dwithin',
                        },
                    },
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


class BaseDetailsView(DjangoDetailView, BaseModelView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update(self._get_render_context(context))
        return self.render_to_response(context)


# class BaseMapView(GeoJSONResponseMixin):
#
#     map_settings = MAP_SETTINGS
#
#     def _get_render_context(self, context={}):
#         ctx = super()._get_render_context(context)
#         ctx['map_settings'] = self.map_settings
#         return ctx
#
#     @method_decorator(gzip_page)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


# FINAL VIEWS

class CreateView(DjangoCreateView, BaseFormModelView):

    template_name = 'djaesy/crud/create.html'

    action_title = _('Criar')
    update_url = ''

    option_sidebar = False
    option_footer = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_render_context(context))
        return context

    def get_form_class(self):
        return self._get_form_class()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            formsets = getattr(form, 'formsets', [])
            valid_formsets = True
            for formset in formsets:
                if not formset.is_valid():
                    valid_formsets = False
            if valid_formsets:
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""

        save_and_add_other = self.request.POST.get('new_action', None)
        need_cropping = getattr(self.model, 'ratio_fields', ())

        self.object = form.save()

        formsets = getattr(form, 'formsets', [])
        for formset in formsets:
            formset.instance = self.object
            formset.save()

        if save_and_add_other:
            messages.add_message(self.request, messages.SUCCESS, _('Item criado com sucesso'), extra_tags='success')
            return self.render_to_response(self.get_context_data(form=form))

        elif need_cropping:
            for img_field, crop in self.object.crop_fields.items():
                if getattr(self.object, img_field, None):
                    messages.add_message(
                        self.request, messages.SUCCESS, _('Selecione a área da imagem'), extra_tags='info'
                    )
                    return HttpResponseRedirect(reverse_lazy(self.update_url, kwargs={'pk': self.object.id}))

        return HttpResponseRedirect(self.get_success_url())


class UpdateView(DjangoUpdateView, BaseFormModelView):

    template_name = 'djaesy/crud/update.html'
    action_title = _('Editar')

    option_sidebar = False
    option_footer = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_render_context(context))
        return context

    def get_form_class(self):
        return self._get_form_class()

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""

        save_and_continue = self.request.POST.get('new_action', None)
        response = super().form_valid(form)

        if getattr(self.object, 'ratio_fields', []):
            if self.object.need_cropping():
                save_and_continue = True

        formsets = getattr(form, 'formsets', [])
        for formset in formsets:
            if not formset.is_valid():
                return self.form_invalid(form)
            formset.instance = self.object
            formset.save()

        if save_and_continue:
            return HttpResponseRedirect(self.request.path)

        return response

    def get(self, request, *args, **kwargs):
        # Verifico permissao, redireciono para a pagina "nao tem permissao"
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # permission, permissions_by_model = get_permission(permission_type='change', model=self.model)
        #
        # if not permission or request.user.has_perm(permission):

        return super().post(request, *args, **kwargs)
        # Verifico permissao, redireciono para a pagina "nao tem permissao"


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


# class MapListView(BaseMapView, TableListView):
#
#     template_name = 'djaesy/map/base.html'
#     map_settings = MAP_SETTINGS
#
#     def get_queryset(self):
#         qs = super().get_queryset().exclude(**{self.geometry_field: None})
#         if 'json' in self.request.GET:
#             if isinstance(self.properties, (list, tuple)):
#                 columns = ['pk', self.geometry_field] + list(self.properties)
#                 qs = qs.values(columns)
#             elif isinstance(self.properties, dict):
#                 columns = ['pk', self.geometry_field] + list(self.properties.keys())
#                 qs = qs.values(*columns)
#         return qs
#
#     def get(self, request, *args, **kwargs):
#
#         filterset_class = self.get_filterset_class()
#         self.filterset = self.get_filterset(filterset_class)
#
#         if not self.filterset.is_bound or self.filterset.is_valid() or not self.get_strict():
#             self.object_list = self.filterset.qs
#         else:
#             self.object_list = self.filterset.queryset.none()
#
#         context = self.get_context_data(filter=self.filterset, object_list=self.object_list)
#
#         if 'json' in request.GET:
#             response = self.render_to_response(context)
#             content = orjson.loads(response.content)
#             content = self.statistics(content)
#             response.content = orjson.dumps(content, default=DjangoGeoJSONEncoder().default, option=orjson.OPT_NAIVE_UTC)
#             return response
#         else:
#             self.response_class = TemplateResponse
#             return super(BaseListView, self).render_to_response(context)
#
#     def statistics(self, content):
#         return content
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = {}
#         if 'json' not in self.request.GET:
#             context = super().get_context_data(object_list=object_list, **kwargs)
#             context['list_table'] = self.build_table(context['object_list'])
#             context['page_sizes'] = self.page_sizes
#             if context['is_paginated']:
#                 context['paginator_range'] = self.get_page_range(
#                     context['page_obj'].number, 5, context['paginator'].num_pages
#                 )
#                 context['page_size'] = context['paginator'].per_page
#             else:
#                 context['page_size'] = int(self.request.GET.get('page_size', 0)) or self.paginate_by
#         else:
#             pass
#             # context = super().get_context_data(object_list=object_list, **kwargs)
#         context.update(self._get_render_context(context))
#         return context
#
#
# class MapDetailsView(BaseDetailsView):
#
#     template_name = 'djaesy/map/base.html'
#     map_settings = MAP_SETTINGS
#
#     # geoJsonSettings
#     properties = []
#     precision = None
#     simplify = None
#     srid = GEOJSON_DEFAULT_SRID
#     geometry_field = 'geom'
#     force2d = False
#     bbox = None
#     bbox_auto = False
#     use_natural_keys = False
#     with_modelname = True
#
#     def _get_render_context(self, context={}):
#         ctx = super()._get_render_context(context)
#         ctx['map_settings'] = self.map_settings
#         return ctx
#
#     @method_decorator(gzip_page)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         if 'json' in request.GET:
#             geojson_data = self.geojson_response()
#             return HttpGeoJSONResponse(content=geojson_data)
#         else:
#             return super().get(request, *args, **kwargs)
#
#     def geojson_response(self):
#         raise NotImplementedError('Please implement geojson_reponse')
#
#     def statistics(self, content):
#         return content


class FormView(DjangoFormView, BaseView):

    option_footer = True
    form_layout = None
    form_helper = None

    use_col_class = True
    form_col_xs = 12
    form_col_sm = 6
    form_col_md = 4
    form_col_lg = 3

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        context = super().get_context_data(**kwargs)
        context['form_helper'] = self.form_helper
        return self._get_render_context(context)

    def get_form_class(self):
        """Return the form class to use."""
        form_class = self._setup_helper(self.form_class)
        return form_class

    def _setup_helper(self, form_class=None):

        if self.form_helper:
            helper = self.form_helper
        else:
            helper = FormHelper()
            helper.form_show_labels = True
            helper.form_tag = False
            helper.include_media = False
            # helper.form_show_errors = False
            if self.form_layout:
                helper.layout = self.form_layout
            elif self.use_col_class:
                helper.col_class = f'col col-{self.form_col_xs} col-sm-{self.form_col_sm} col-md-{self.form_col_md} ' \
                                   f'col-lg-{self.form_col_lg}'

        self.form_helper = helper

        return form_class


# COMBO VIEWS

class CrudCombo:

    model = None
    url_name_prefix = ''
    icon = ''
    form_layout = None
    menu_title = ''

    relationships = []
    permission = ''

    #Combo
    _list = None
    _create = None
    _update = None

    def _get_crud_class(self, class_name):

        assert class_name in ['List', 'Create', 'Update']
        crud_class = getattr(self, class_name, None)

        if not crud_class:
            if class_name == 'List':
                class List(TableListView):
                    relationships = self.relationships
                    permission = self.permission
                return List
            elif class_name == 'Create':
                class Create(CreateView):
                    relationships = self.relationships
                    permission = self.permission
                return Create
            elif class_name == 'Update':
                class Update(UpdateView):
                    relationships = self.relationships
                    permission = self.permission
                return Update
        else:
            crud_class.relationships = self.relationships
            crud_class.permission = self.permission
            return crud_class

    def __init__(self):

        if not self.url_name_prefix:
            self.url_name_prefix = slugify(self.model.__name__)

        mlist = self._get_crud_class('List')
        mlist.model = self.model
        mlist.create_url_name = f'{self.url_name_prefix}_create'
        mlist.update_url_name = f'{self.url_name_prefix}_update'

        update = self._get_crud_class('Update')
        update.model = self.model
        update.back_url_name = f'{self.url_name_prefix}_list'
        update.success_url = reverse_lazy(f'{self.url_name_prefix}_list')

        create = self._get_crud_class('Create')
        create.model = self.model
        create.back_url_name = f'{self.url_name_prefix}_list'
        create.update_url = f'{self.url_name_prefix}_update'
        create.success_url = reverse_lazy(f'{self.url_name_prefix}_list')

        if self.icon:
            mlist.icon = self.icon
            create.icon = self.icon
            update.icon = self.icon

        if self.form_layout:
            create.form_layout = self.form_layout
            update.form_layout = self.form_layout

        self._list = mlist
        self._create = create
        self._update = update

    @property
    def urls(self):
        try:
            add_permission, permissions_by_model = get_permission(permission_type='add', model=self.model)
            view_permission, permissions_by_model = get_permission(permission_type='view', model=self.model)
            change_permission, permissions_by_model = get_permission(permission_type='change', model=self.model)

            return [
                path(
                    f'{self.url_name_prefix}/create',
                    permission_required(add_permission)(self._create.as_view()),
                    name=f'{self.url_name_prefix}_create'
                ),
                path(
                    f'{self.url_name_prefix}/update/<pk>',
                    permission_required(change_permission)(self._update.as_view()),
                    name=f'{self.url_name_prefix}_update'
                ),
                path(
                    f'{self.url_name_prefix}/list',
                    permission_required(view_permission)(self._list.as_view()),
                    name=f'{self.url_name_prefix}_list'
                )
            ]
        except Exception as e:
            return []

    def load_menus(self, menu='main', create_link=False, get_children=False):

        vn = self._list()._get_verbose_names()
        menu_title = self.menu_title or vn['verbose_name_plural']

        children = [
            MenuItem(title=menu_title, url=f'{self.url_name_prefix}_list', icon=self._list.icon),
        ]

        if create_link:
            children.append(MenuItem(
                title=f'Criar {vn["verbose_name"]}', url=f'{self.url_name_prefix}_create',
                icon=self._create.icon
            ))

        if not get_children:
            Menu.add_item(
                menu,
                MenuItem(
                    title=menu_title, url=f'{self.url_name_prefix}_list', no_link=True,
                    icon=self._list.icon, children=children
                )
            )
        else:
            return children

