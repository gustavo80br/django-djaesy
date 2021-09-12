# import orjson

from django.conf import settings
from django.contrib import messages
# from django.contrib.gis.forms import PointField
from django.db.models.deletion import ProtectedError
from django.shortcuts import render
# from django.template.response import TemplateResponse
# from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from djaesy.actions.forms import ConfirmActionForm, BaseActionForm
from djaesy.security.permission import get_permission


# from django.views.decorators.gzip import gzip_page
# from djgeojson import GEOJSON_DEFAULT_SRID
# from djgeojson.http import HttpGeoJSONResponse
# from djgeojson.serializers import DjangoGeoJSONEncoder
# from djgeojson.views import GeoJSONResponseMixin
# from numpy import datetime64
from djaesy.actions.views import Action
from djaesy.core.views.base import BaseView


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