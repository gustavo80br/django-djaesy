from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeDoneView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse

from djaesy.base_views import BaseView, BaseFormModelView


class Login(LoginView):

    template_name = 'djaesy/login/login.html'

    class LoginForm(AuthenticationForm):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.error_messages['invalid_login'] = _('Login Inválido')

            self.helper = FormHelper()
            self.helper.form_show_labels = False
            self.helper.form_id = 'login-form'
            self.helper.form_class = 'login'
            self.helper.layout = Layout(
                Div(Field(
                    'username', placeholder=_('Email'), css_class="form-control form-control-user"
                ), css_class="form-group"),
                Div(Field(
                    'password', placeholder=_('Senha'), css_class="form-control form-control-user"
                ), css_class="form-group"),
                Div(Submit('submit', _('Entrar'), css_class='btn btn-block btn-success waves-effect waves-light'))
            )

    authentication_form = LoginForm

    def get(self, request, **kwargs):
        if False and request.user.is_authenticated:
            return redirect(reverse('djaesy_main'))
        else:
            return super().get(self, request, **kwargs)


class ResetPassword(PasswordResetView):

    template_name = 'djaesy/reset-password.html'

    class PasswordForm(PasswordResetForm):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # self.error_messages['invalid_login'] = _('Login Inválido')

            self.helper = FormHelper()
            self.helper.form_show_labels = False
            self.helper.form_id = 'reset-password-form'
            self.helper.form_class = 'reset-password'
            self.helper.layout = Layout(
                Div(Field(
                    'email', placeholder=_('Email'), css_class="form-control form-control-user"
                ), css_class="form-group"),
                Div(Submit(
                    'submit', _('Redefinir Senha'), css_class='btn btn-block btn-success waves-effect waves-light'
                ))
            )

    form_class = PasswordForm


class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'djaesy/reset-password-done.html'


class ResetPasswordConfirm(PasswordResetConfirmView):

    class ResetPasswordForm(SetPasswordForm):

        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)

            self.fields['new_password1'].help_text = ''

            self.helper = FormHelper()
            self.helper.form_show_labels = False
            self.helper.form_id = 'reset-password-form'
            self.helper.form_class = 'reset-password'
            self.helper.layout = Layout(
                Div(
                    Field(
                        'new_password1',
                        placeholder=_('Nova senha'),
                        css_class="form-control form-control-user",
                    ),
                    css_class="form-group"
                ),
                Div(
                    Field(
                        'new_password2',
                        placeholder=_('Repita a nova senha'),
                        css_class="form-control form-control-user"
                    ),
                    css_class="form-group"
                ),
                Div(
                    Submit('submit', _('Redefinir Senha'),
                    css_class='btn btn-block btn-success waves-effect waves-light')
                )
            )

    form_class = ResetPasswordForm
    template_name = 'djaesy/reset-password-confirm.html'
    title = _('Enter new password')


class ResetPasswordComplete(PasswordResetCompleteView):

    template_name = 'djaesy/reset-password-complete.html'


class ChangePassword(PasswordChangeView, BaseFormModelView):

    page_title = _('Mudar Senha')
    content_title = _('Mudar Senha')

    class Form(PasswordChangeForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['new_password1'].help_text = ''

    form_class = Form

    def get_form_kwargs(self):
        super()._setup_helper()
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_render_context())
        return context


class ChangePasswordDone(PasswordChangeDoneView, BaseView):

    page_title = _('Senha Alterada')
    content_title = _('Senha Alterada com Sucesso!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_render_context())
        return context
