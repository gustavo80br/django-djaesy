from crum import get_current_user
from django import forms
from django.apps import apps
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

import djaesy
from djaesy.security.models import Role
from djaesy.security.permission import check_permissions, permission_tuple

permissions = djaesy.security.permission.permissions


class BaseActionForm(forms.Form):
    action_form = forms.IntegerField(widget=forms.HiddenInput())
    selected_items = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class': 'selected-items-field'}))


class ConfirmActionForm(BaseActionForm):
    pass


class StrongConfirmActionForm(BaseActionForm):
    pass
