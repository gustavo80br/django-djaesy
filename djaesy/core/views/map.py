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

from djaesy.autocomplete.widgets import ModelSelect2, ModelSelect2Multiple
from djaesy.actions.forms import ConfirmActionForm, BaseActionForm
from djaesy.menus.engine import Menu, MenuItem
from djaesy.security.permission import get_permission

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





# BASE VIEWS












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






