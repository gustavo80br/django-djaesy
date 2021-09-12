from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from djaesy.menus.engine import Menu, MenuItem
from djaesy.menus_pkg.app import AppMenu

if settings.DJAESY_USER_MENU:

    Menu.add_item(
        "main",
        MenuItem(
            _('Usuários'), 'user_list', no_link=True, icon='mdi mdi-account-multiple',
            children=[
                MenuItem(title=_('Usuários'), url='user_list', icon='mdi mdi-account-multiple'),
                MenuItem(title=_('Perfis'), url='user_role_list', icon='mdi mdi-account-outline'),
            ]
        ),
    )

AppMenu.app({
    "main": {
        "users": {
            "add_user": {

            },
            "remove_user": {

            }
        }
    },
})
