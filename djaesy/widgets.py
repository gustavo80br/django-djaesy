# import json
# from venv import logger

# from django.contrib.gis.geos import GEOSGeometry, GEOSException
from django.forms.widgets import Input
from leaflet.forms.widgets import LeafletWidget

# from djaesy.geos import circle_maker
from djaesy.autocomplete import ModelSelect2Multiple


class CustomClassInput(Input):

    widget_class = ''
    icon = ''

    def __init__(self, attrs=None, **kwargs):

        if attrs is None:
            attrs = {}

        for arg, value in kwargs.items():
            if arg != 'attrs':
                if value:
                    arg = arg.replace('_', '-')
                    attrs[f'data-{arg}'] = f'{str(value)}'

        if attrs is not None:
            classes = attrs.get('class', '')
            classes += f' {self.widget_class}'
            attrs['class'] = classes
        else:
            attrs = {'class': self.widget_class}
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['icon'] = self.icon or 'mdi mdi-calendar'
        return context


class YearPicker(CustomClassInput):

    widget_class = 'widget-yearpicker '
    template_name = 'djaesy/widgets/datetimepicker.html'

    def __init__(self, attrs=None, max_year=None, min_year=None):
        if max_year:
            max_year = f'01-01-{max_year}'
        if min_year:
            min_year = f'01-01-{min_year}'
        super().__init__(attrs, max_date=max_year, min_date=min_year, view_mode='years', format='YYYY')


class DatePicker(CustomClassInput):

    widget_class = 'widget-datepicker '
    template_name = 'djaesy/widgets/datetimepicker.html'
    icon = 'mdi mdi-calendar-month'

    def __init__(self, attrs=None, max_date=None, min_date=None):
        max_date = max_date.isoformat() if max_date else None
        min_date = min_date.isoformat() if min_date else None
        super().__init__(attrs, max_date=max_date, min_date=min_date, view_mode='days', format='DD/MM/YYYY', use_current='false')


class DateRange(CustomClassInput):
    widget_class = 'widget-datepicker'


class DateTimePicker(CustomClassInput):
    widget_class = 'widget-datetimepicker'


class DateRangePicker(CustomClassInput):
    widget_class = 'widget-daterangepicker'

    def get_context(self, name, value, attrs):
        if value:
            if isinstance(value, str):
                attrs['data-start-date'], attrs['data-end-date'] = value.split(' - ')
            else:
                attrs['data-start-date'] = value[0].strftime('%d/%m/%y %H:%M')
                attrs['data-end-date'] = value[1].strftime('%d/%m/%y %H:%M')
            attrs['data-drops'] = 'down'
            value = f"{attrs['data-start-date']} - {attrs['data-end-date']}"
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context


class MultiSelectBox(ModelSelect2Multiple):
    autocomplete_function = 'your-autocomplete-function'


# class SinglePolygonDraw(LeafletWidget):
#
#     geometry_field_class = 'SinglePolygonGeometryField'
#
#     # settings_overrides = {
#     #     'TILES': [
#     #         (
#     #             'Ruas',
#     #             'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
#     #             {
#     #                 'attribution': 'OpenStreetMap'
#     #             }
#     #         ),
#     #         (
#     #             'Satelite',
#     #             'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#     #             {
#     #                 'attribution': 'ArcGIS Online',
#     #                 'maxZoom': 17
#     #             }
#     #         ),
#     #         (
#     #             'Relevo',
#     #             'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
#     #             {
#     #                 'attribution': 'ArcGIS Online'
#     #             }
#     #         ),
#     #
#     #     ],
#     #     'ATTRIBUTION_PREFIX': '<a href="https://i3track.com.br">i3Track ®</a>',
#     #     'DEFAULT_CENTER': (-22.2864684, -45.8961274),
#     #     'DEFAULT_ZOOM': 10,
#     #     'MIN_ZOOM': 8,
#     #     'MAX_ZOOM': 17,
#     # }
#
#     def __init__(self, settings={}, *args, **kwargs):
#         if settings:
#             self.settings_overrides = settings
#         super().__init__(*args, **kwargs)
#
#     def deserialize(self, value):
#
#         values = json.loads(value)
#         geometry = values.get('geometry', None)
#         properties = values.get('properties', {})
#
#         if not geometry:
#             return None
#         else:
#             geo_type = geometry.get('type', None)
#             if not geo_type:
#                 return None
#         try:
#             if 'radius' in properties and geo_type == 'Point':
#                 return circle_maker(geometry['coordinates'], properties['radius'])
#             else:
#                 value = json.dumps(geometry)
#                 return GEOSGeometry(value)
#         except (GEOSException, ValueError, TypeError) as err:
#             logger.error("Error creating geometry from value '%s' (%s)", value, err)
#         return None

