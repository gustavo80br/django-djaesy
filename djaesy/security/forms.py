from crum import get_current_user
from django import forms
from django.apps import apps
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _

import djaesy
from djaesy.security.models import Role
from djaesy.security.permission import check_permissions, permission_tuple

permissions = djaesy.security.permission.permissions


class BaseRoleForm(ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        check_permissions()
        user = get_current_user()
        instance = kwargs.get('instance', None)
        models_codename_permissions = []

        if instance:
            # Get all permissions saved to set checkbox with initial values
            permissions_by_role = kwargs['instance'].permissions.all()
            models_codename_permissions = list(
                permissions_by_role.values_list('content_type__model', 'codename').distinct()
            )

        group_id = 0
        for group in permissions:

            entities = group.get('entities', None)
            if entities and user:
                if user.relationship not in entities and user.relationship > 0:
                    continue

            permission_items = []
            initial_permissions = []
            for item in group['permissions']:

                show_permission = True
                try:
                    entities = item[2:3] or None
                    if entities:
                        entities = entities[0]
                        assert isinstance(entities, (tuple, list))
                        show_permission = bool(user.relationship in entities)
                except:
                    raise ImproperlyConfigured('Permission item is not a valid list')

                if show_permission:
                    permission_items.append((item[0], item[1]))

                if instance:
                    perm_tuple = permission_tuple(item[0])
                    if perm_tuple in models_codename_permissions:
                        initial_permissions.append(item[0])

            group_id += 1
            key = f'permission_group_{group_id}'
            self.fields[key] = forms.MultipleChoiceField(
                required=False,
                widget=forms.CheckboxSelectMultiple,
                choices=permission_items,
                label=group['label']
            )

            if initial_permissions:
                self.fields[key].initial = initial_permissions

    def set_permissions_to_role(self):
        try:
            self.instance.permissions.clear()
            for item in self.cleaned_data:
                if isinstance(self.cleaned_data[item], list):
                    for item2 in self.cleaned_data[item]:
                        permission_key = item2
                        perm_key = permission_key.split('.')
                        app_label = perm_key[0]
                        model_name = perm_key[1]
                        codename = perm_key[2]
                        ct = ContentType.objects.get_for_model(
                            apps.get_model(app_label=app_label, model_name=model_name)
                        )
                        permissions_by_model = Permission.objects.filter(content_type=ct)
                        try:
                            permission = permissions_by_model.get(codename=codename)
                            self.instance.permissions.add(permission)
                        except Permission.DoesNotExist:
                            pass
        except Exception as e:
            raise Exception(f'CreateRoleForm.clean: {e}')

    def save(self, *args, **kwargs):
        obj = super(BaseRoleForm, self).save(*args, **kwargs)
        self.set_permissions_to_role()
        return obj


class CreateRoleForm(BaseRoleForm):

    class Meta:
        model = Role
        fields = ['name']


class UpdateRoleForm(BaseRoleForm):

    class Meta:
        model = Role
        fields = ['name']


class UserCreationForm(forms.ModelForm):
    """A form that creates a user, with no privileges, from the given username and password."""
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Confirme a Senha"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = get_user_model()
        exclude = ('date_joined', 'password', 'is_superuser', 'is_staff', 'last_login')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):

    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        # help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False
    )

    class Meta:
        model = get_user_model()
        exclude = ('date_joined', 'password', 'is_superuser', 'is_staff', 'last_login')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if (password1 or password2) and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super(UserUpdateForm, self)._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user