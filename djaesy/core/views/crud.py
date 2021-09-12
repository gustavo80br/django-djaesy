# -*- coding: utf-8 -*-

# CHECK THIS OUT: https://ccbv.co.uk/

# import orjson

from django.contrib.auth.decorators import permission_required
# from django.contrib.gis.forms import PointField
# from django.template.response import TemplateResponse
from django.urls import reverse_lazy, path
# from django.utils.decorators import method_decorator
from django.utils.text import slugify

from djaesy.menus.engine import Menu, MenuItem
from djaesy.security.permission import get_permission


# from django.views.decorators.gzip import gzip_page
# from djgeojson import GEOJSON_DEFAULT_SRID
# from djgeojson.http import HttpGeoJSONResponse
# from djgeojson.serializers import DjangoGeoJSONEncoder
# from djgeojson.views import GeoJSONResponseMixin
# from numpy import datetime64

# from silk.profiling.profiler import silk_profile


# https://django-leaflet.readthedocs.io/en/latest/templates.html#use-leaflet-api
# https://cloud.maptiler.com/ (google account gustavo@fundacaoaprender.org.br)
# https://www.arcgis.com/home/webmap/viewer.html

# TODO: Individualizar Geo funcoes'
from djaesy.core.views.form import CreateView, UpdateView
from djaesy.core.views.table import TableListView


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
        except Exception as _:
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

