from django.utils.translation import ugettext_lazy as _

from menus.engine import menu_combo
from sandbox.views import TabBView, TabAView


# menu_combo([
#     TabBView,
#     TabAView
# ], title=_('Teste'), icon='mdi mdi-bell-ring-outline')

# Menu.add_item(
#     "main",
#     MenuItem(
#         _('Monitoramento'), 'vehicles_monitoring', no_link=True, icon='mdi mdi-access-point',
#         children=[
#             MenuItem(title=_('Mapa'), url='vehicles_map', icon='mdi mdi-map'),
#             MenuItem(title=_('Monitoramento'), url='vehicles_monitoring', icon='mdi mdi-access-point'),
#         ]
#     ),
# )