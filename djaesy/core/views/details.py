# import orjson

# from django.contrib.gis.forms import PointField
# from django.template.response import TemplateResponse
# from django.utils.decorators import method_decorator
# from django.views.decorators.gzip import gzip_page
from django.views.generic import DetailView as DjangoDetailView

# from djgeojson import GEOJSON_DEFAULT_SRID
# from djgeojson.http import HttpGeoJSONResponse
# from djgeojson.serializers import DjangoGeoJSONEncoder
# from djgeojson.views import GeoJSONResponseMixin
# from numpy import datetime64
from djaesy.core.views.model import BaseModelView


class BaseDetailsView(DjangoDetailView, BaseModelView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update(self._get_render_context(context))
        return self.render_to_response(context)
