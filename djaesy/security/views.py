import django_filters
from crispy_forms.layout import Div, Layout, HTML
from crum import get_current_user
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from djaesy.security.layouts import USER_CREATE_EDIT_LAYOUT
from djaesy.security.login_views import ChangePassword, ChangePasswordDone
from djaesy.security.models import Role
from djaesy.utils import load_form
from djaesy.security.forms import UserCreationForm, UserUpdateForm, CreateRoleForm, UpdateRoleForm
from djaesy.core.views.form import CreateView, UpdateView
from djaesy.core.views.table import TableListView


user_creation_form = getattr(settings, 'DJAESY_USER_CREATE_FORM', UserCreationForm)
if isinstance(user_creation_form, str):
    user_creation_form = load_form(user_creation_form)

user_update_form = getattr(settings, 'DJAESY_USER_UPDATE_FORM', UserUpdateForm)
if isinstance(user_update_form, str):
    user_update_form = load_form(user_update_form)


class UserList(TableListView):

    model = get_user_model()
    create_url_name = 'user_create'
    update_url_name = 'user_update'

    paginate_by = 50

    icon = 'mdi mdi-account-multiple'

    table_columns = ['email', 'name', 'role__name']

    filter_by = ['role', 'email', 'name']

    declared_filters = (
        django_filters.CharFilter(label=_("Email"), field_name='email', lookup_expr='icontains'),
        django_filters.CharFilter(label=_("Nome"), field_name='name', lookup_expr='icontains'),
    )


class UserCreate(CreateView):

    model = get_user_model()
    back_url_name = 'user_list'
    icon = 'mdi mdi-account-plus'
    form_class = user_creation_form
    success_url = reverse_lazy('user_list')

    def _setup_helper(self, form_class=None):
        self.form_layout = getattr(settings, 'DJAESY_USER_CREATE_LAYOUT', USER_CREATE_EDIT_LAYOUT)
        super()._setup_helper(form_class)
        return form_class


class UserUpdate(UpdateView):

    model = get_user_model()
    back_url_name = 'user_list'
    icon = 'mdi mdi-account-edit'
    form_class = user_update_form
    success_url = reverse_lazy('user_list')

    def _setup_helper(self, form_class=None):
        self.form_layout = getattr(settings, 'DJAESY_USER_UPDATE_LAYOUT', USER_CREATE_EDIT_LAYOUT)
        super()._setup_helper(form_class)
        return form_class


class UserChangePassword(ChangePassword):

    template_name = 'djaesy/user/user-change-password.html'
    icon = 'mdi mdi-shield-lock'
    success_url = reverse_lazy('user_change_password_done')

    option_menubar_open = False
    option_menubar_toggle = True
    option_sidebar_open = True

    option_fluid_layout = False
    option_sm_layout_size = 12
    option_md_layout_size = 8
    option_lg_layout_size = 6
    option_xl_layout_size = 4

    form_col_sm = 12
    form_col_md = 12
    form_col_lg = 12

    option_sidebar_icon = 'mdi mdi-shield-alert-outline'
    option_side_help_title = 'Segurança'
    option_side_help_icon = ''
    option_side_help = _("""
    <p>Sua senha é de uso pessoal e exclusivo, deve seguir algumas regras:
    <ul>
        <li>Conter pelo menos 8 caracteres.</li>
        <li>Não ser inteiramente numérica</li>
        <li>Não ser similar às suas informações pessoais.</li>
        <li>Não ser uma senha muito comunmente usada.</li>
    </ul>
    """)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_render_context())
        return context

    def form_valid(self, form):
        user = get_current_user()
        if getattr(user, 'must_change_password', False):
            user.must_change_password = False
            user.save()
        return super().form_valid(form)


class UserChangePasswordDone(ChangePasswordDone):

    template_name = 'djaesy/user/user-change-password-done.html'
    icon = 'mdi mdi-shield-lock'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_titles())
        context.update(self._get_render_context())
        return context


class RoleList(TableListView):

    model = Role
    create_url_name = 'user_role_create'
    update_url_name = 'user_role_update'

    paginate_by = 50

    icon = 'mdi mdi-account-outline'

    ordering = 'name'
    table_columns = ['name']
    filter_by = ['name']

    declared_filters = (
        django_filters.CharFilter(field_name='name', lookup_expr='icontains'),
    )


class RoleCreate(CreateView):

    form_class = CreateRoleForm

    template_name = 'djaesy/crud/create.html'
    back_url_name = 'user_role_list'

    icon = 'mdi mdi-shield-account-outline'
    content_title = 'Criar Perfil de Usuário'
    page_title = 'Criar Perfil de Usuário'

    success_url = reverse_lazy('user_role_list')

    def _setup_helper(self, form_class=None):

        layout = [
            Div(
                Div(
                    Div('name', css_class="col col-3"),
                    css_class='row'
                ),
                css_class='col col-12 col-sm-12 col-md-12'
            ),
            Div(
                HTML('<hr/>'),
                css_class='col col-12'
            ),
        ]

        permission_fields = self.form_class().fields
        permission_sizes = [
            (field, len(item.choices)) for field, item in permission_fields.items() if field.startswith('permission_')
        ]
        permission_sizes.sort(key=lambda permission_sizes: permission_sizes[1])

        for field in permission_sizes:
            layout.append(
                Div(field[0], css_class="col col-3 permission-checkbox-group"),
            )

        self.form_layout = Layout(*layout)
        return super()._setup_helper(form_class)


class RoleUpdate(UpdateView):

    form_class = UpdateRoleForm
    model = Role

    template_name = 'djaesy/crud/update.html'
    back_url_name = 'user_role_list'

    icon = 'mdi mdi-shield-account-outline'
    content_title = 'Editar Perfil de Usuário'
    page_title = 'Editar Perfil de Usuário'

    success_url = reverse_lazy('user_role_list')

    def _setup_helper(self, form_class=None):
        layout = [
            Div(
                Div(
                    Div('name', css_class="col col-3"),
                    css_class='row'
                ),
                css_class='col col-12 col-sm-12 col-md-12'
            ),
            Div(
                HTML('<hr/>'),
                css_class='col col-12'
            ),
        ]

        permission_fields = self.form_class().fields

        for field in permission_fields:
            if field.startswith('permission_'):
                layout.append(
                    Div(field, css_class="col col-3 permission-checkbox-group"),
                )
        self.form_layout = Layout(*layout)
        return super()._setup_helper(form_class)