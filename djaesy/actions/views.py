# import orjson

# from django.contrib.gis.forms import PointField
from django.core.exceptions import ImproperlyConfigured

from djaesy.actions.forms import BaseActionForm
from djaesy.security.permission import get_permission


# from django.template.response import TemplateResponse
# from django.utils.decorators import method_decorator
# from django.views.decorators.gzip import gzip_page
# from djgeojson import GEOJSON_DEFAULT_SRID
# from djgeojson.http import HttpGeoJSONResponse
# from djgeojson.serializers import DjangoGeoJSONEncoder
# from djgeojson.views import GeoJSONResponseMixin
# from numpy import datetime64

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
