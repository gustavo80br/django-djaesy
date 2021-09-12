import json

from crispy_forms.helper import FormHelper
from django.contrib import messages
# from django.contrib.gis.forms import PointField
from django.core.exceptions import ImproperlyConfigured
from django.forms import models as model_forms
from django.http import HttpResponseRedirect
# from django.template.response import TemplateResponse
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
# from django.views.decorators.gzip import gzip_page
from django.views.generic import CreateView as DjangoCreateView
from django.views.generic import FormView as DjangoFormView
from django.views.generic import UpdateView as DjangoUpdateView

from djaesy.autocomplete.widgets import ModelSelect2, ModelSelect2Multiple
from djaesy.core.views.base import BaseView
from djaesy.core.views.model import BaseModelView


# import orjson
# from djgeojson import GEOJSON_DEFAULT_SRID
# from djgeojson.http import HttpGeoJSONResponse
# from djgeojson.serializers import DjangoGeoJSONEncoder
# from djgeojson.views import GeoJSONResponseMixin
# from numpy import datetime64


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