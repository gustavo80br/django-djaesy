# Create your tests here.

from djaesy.menus.app import AppMenu

# PROJECT MENU

#   APP 1 MENU
#       APP-1-A
#       APP-1-B
#       APP-1-C

#   APP 2 MENU
#       APP-2-A
#       APP-2-B
#       APP-2-C

#   APP 3 MENU
#       APP-3-A
#       APP-3-B
#       APP-3-C

#   NO APP MENU
#       APP-1-A
#       APP-2-B
#       APP-3-C

def test_menu_tree():

    # First app menu - Restaurant Menu
    AppMenu.app({
        'restaurant-service': {
            'menu-setup': {
                'create-menu': {},
                'add-menu-item': {},
                'price-tables': {},
                'promotions': {}
            }
        },
    })

    # Second app menu - Restaurante Client management
    AppMenu.app({
        'restaurant-service': {
            'clients': {
                'create-menu': {},
                'add-menu-item': {},
                'price-tables': {},
                'promotions': {}
            }
        },
    })


