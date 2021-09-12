# import orjson

from django.conf import settings
# from django.contrib.gis.forms import PointField
from django.shortcuts import render
# from django.template.response import TemplateResponse
# from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views import View
# from django.views.decorators.gzip import gzip_page
# from djgeojson import GEOJSON_DEFAULT_SRID
# from djgeojson.http import HttpGeoJSONResponse
# from djgeojson.serializers import DjangoGeoJSONEncoder
# from djgeojson.views import GeoJSONResponseMixin
# from numpy import datetime64


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