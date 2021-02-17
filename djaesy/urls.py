from django.conf import settings
from django.conf.urls import i18n
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path

from djaesy.base_views import BaseView
from djaesy.login_views import Login, ResetPassword, ResetPasswordDone, ResetPasswordConfirm, \
    ResetPasswordComplete
from djaesy.utils import load_view
from djaesy.views import UserList, UserCreate, UserUpdate, UserChangePassword, UserChangePasswordDone, \
    RoleList, RoleCreate, RoleUpdate, SetLanguage, DjaesyTabViewWrapper

user_list_view = getattr(settings, 'DJAESY_USER_LIST_VIEW', UserList)
user_create_view = getattr(settings, 'DJAESY_USER_CREATE_VIEW', UserCreate)
user_update_view = getattr(settings, 'DJAESY_USER_UPDATE_VIEW', UserUpdate)

if isinstance(user_list_view, str):
    user_list_view = load_view(user_list_view)
if isinstance(user_create_view, str):
    user_create_view = load_view(user_create_view)
if isinstance(user_update_view, str):
    user_update_view = load_view(user_update_view)

urlpatterns = [

    # path('', login_required(BaseView.as_view()), name='djaesy_main'),

    re_path('app/(?P<path>.*)$', login_required(DjaesyTabViewWrapper.as_view()), name='djaesy_tabview'),

    # path('map/test', MapListView.as_view(), name='map_test'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('login/reset-password', ResetPassword.as_view(), name='login_reset_password'),
    path('login/reset-password/success', ResetPasswordDone.as_view(), name='password_reset_done'),
    path('login/reset-password-confirm/<uidb64>/<token>/', ResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    path('login/reset-password-complete', ResetPasswordComplete.as_view(), name='password_reset_complete'),

    path('user/list', login_required(user_list_view.as_view()), name='user_list'),
    path('user/create', login_required(user_create_view.as_view()), name='user_create'),
    path('user/update/<pk>', login_required(user_update_view.as_view()), name='user_update'),
    path('user/change-password', login_required(UserChangePassword.as_view()), name='user_change_password'),
    path('user/change-password/success', login_required(UserChangePasswordDone.as_view()), name='user_change_password_done'),

    path('user/role/list', login_required(RoleList.as_view()), name='user_role_list'),
    path('user/role/create', login_required(RoleCreate.as_view()), name='user_role_create'),
    path('user/role/update/<pk>', login_required(RoleUpdate.as_view()), name='user_role_update'),

    path('i18n/', include('django.conf.urls.i18n')),

]