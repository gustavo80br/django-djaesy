import copy

from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.utils.text import slugify

from djaesy.security.permission import get_permission
from djaesy.utils import get_view_from_url

try:
    from django.apps import apps
except ImportError:
    apps = False


class Menu(object):
    """
    Menu is a class that generates menus

    It allows for multiple named menus, which can be accessed in your templates
    using the generate_menu template tag.

    Menus are loaded from the INSTALLED_APPS, inside a file named menus.old.py.
    This file should import the Menu & MenuItem classes and then call add_item:

        Menu.add_item("main", MenuItem("My item",
                                       reverse("myapp.views.myview"),
                                       weight=10))

    Note: You cannot have the same URL in a MenuItem in different
    Menus, but it is not enforced. If you do submenus will not work
    properly.
    """
    items = {}
    sorted = {}
    loaded = False

    @classmethod
    def add_item(c, name, item):
        """
        add_item adds MenuItems to the menu identified by 'name'
        """
        if isinstance(item, MenuItem):
            if name not in c.items:
                c.items[name] = []
            c.items[name].append(item)
            c.sorted[name] = False

    @classmethod
    def load_menus(c):
        """
        load_menus loops through INSTALLED_APPS and loads the menu.py
        files from them.
        """

        # we don't need to do this more than once
        if c.loaded:
            return

        # Fetch all installed app names
        app_names = settings.INSTALLED_APPS
        if apps:
            app_names = [
                app_config.name
                for app_config in apps.get_app_configs()
            ]

        # loop through our INSTALLED_APPS
        for app in app_names:
            # skip any django apps
            if app.startswith("django."):
                continue

            menu_module = '%s.menus' % app
            try:
                __import__(menu_module, fromlist=["menu", ])
            except ImportError:
                pass

        c.loaded = True

    @classmethod
    def sort_menus(c):
        """
        sort_menus goes through the items and sorts them based on
        their weight
        """
        for name in c.items:
            if not c.sorted[name]:
                c.items[name].sort(key=lambda x: x.weight)
                c.sorted[name] = True

    @classmethod
    def process(c, request, name=None):
        """
        process uses the current request to determine which menus
        should be visible, which are selected, etc.
        """
        # make sure we're loaded & sorted
        c.load_menus()
        c.sort_menus()

        if name is None:
            # special case, process all menus
            items = {}
            for name in c.items:
                items[name] = c.process(request, name)
            return items

        if name not in c.items:
            return []

        items = copy.deepcopy(c.items[name])
        curitem = None
        for item in items:
            item.process(request)
            if item.visible:
                item.selected = False
                if item.match_url(request):
                    if curitem is None or len(curitem.url) < len(item.url):
                        curitem = item

        if curitem is not None:
            curitem.selected = True

        # return only visible items
        visible = [
            item
            for item in items
            if item.visible
        ]

        # determine if we should apply 'selected' to parents when one of their
        # children is the 'selected' menu
        if getattr(settings, 'MENU_SELECT_PARENTS', False):
            def is_child_selected(item):
                for child in item.children:
                    if child.selected or is_child_selected(child):
                        return True

            for item in visible:
                if is_child_selected(item):
                    item.selected = True

        return visible


class MenuItem(object):
    """
    MenuItem represents an item in a menu, possibly one that has a sub-menu (children).
    """

    def __init__(
        self, title, url=None, children=[], weight=1, check=None,  visible=True, slug=None, exact_url=False, **kwargs):
        """
        MenuItem constructor

        title       either a string or a callable to be used for the title
        url         the url of the item
        children    an array of MenuItems that are sub menus to this item
                    this can also be a callable that generates an array
        weight      used to sort adjacent MenuItems
        check       a callable to determine if this item is visible
        slug        used to generate id's in the HTML, auto generated from
                    the title if left as None
        exact_url   normally we check if the url matches the request prefix
                    this requires an exact match if set

        All other keyword arguments passed into the MenuItem constructor are
        assigned to the MenuItem object as attributes so that they may be used
        in your templates. This allows you to attach arbitrary data and use it
        in which ever way suits your menus the best.
        """

        try:
            self.url = reverse(url)
            self.url_name = url
        except NoReverseMatch:
            self.url = url
            self.url_name = None

        self.title = title
        self.visible = visible
        self.children = children
        self.weight = weight
        self.check_func = check
        self.slug = slug
        self.exact_url = exact_url
        self.selected = False
        self.parent = None

        # merge our kwargs into our self
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def check(self, request):
        """
        Evaluate if we should be visible for this request
        """
        try:
            if self.url_name:
                if not self.has_menu_permission(request):
                    self.visible = False

            if callable(self.check_func):
                self.visible = self.check_func(request)
        except Exception as e:
            raise Exception(f'MenuItem.check: {e}')

    def has_menu_permission(self, request):

        view = get_view_from_url(url=self.url)
        user = request.user

        view_relationships = getattr(view, 'relationships', None)
        view_permission = getattr(view, 'permission', None)
        view_model = getattr(view, 'model', None)

        if view_relationships:
            if user.relationship not in view_relationships:
                return False

        if view_permission:
            if view_model:
                permission, permissions_by_model = get_permission(permission_type=view_permission, model=view_model)
            else:
                if '.' in view_permission:
                    perm_key = view_permission.split('.')
                    app_label = perm_key[0]
                    model_name = perm_key[1]
                    codename = perm_key[2]
                    model_instance = apps.get_model(app_label=app_label, model_name=model_name.capitalize())
                    permission, permissions_by_model = get_permission(permission_type=codename, model=model_instance)
                else:
                    raise Exception(
                        f'It is necessary model attribute on view or '
                        f'the permission attribute must contains the complete permission.'
                    )
        else:
            permission, permissions_by_model = get_permission(permission_type='view', model=view_model)

        return user.has_perm(permission)

    def process(self, request):
        """
        process determines if this item should visible, if its selected, etc...
        """
        # if we're not visible we return since we don't need to do anymore processing
        self.check(request)
        if not self.visible:
            return

        # evaluate our title
        if callable(self.title):
            self.title = self.title(request)

        # if no title is set turn it into a slug
        if self.slug is None:
            # in python3 we don't need to convert to unicode, in python2 slugify
            # requires a unicode string
            self.slug = slugify(self.title)

        # evaluate children
        if callable(self.children):
            children = list(self.children(request))
        else:
            children = list(self.children)

        for child in children:
            child.parent = self
            child.process(request)

        self.children = [child for child in children if child.visible]
        self.children.sort(key=lambda child: child.weight)

        # if we have no children and MENU_HIDE_EMPTY then we are not visible and should return
        hide_empty = getattr(settings, 'MENU_HIDE_EMPTY', False)
        if hide_empty and len(self.children) == 0:
            self.visible = False
            return

        # find out if one of our children is selected, and mark it as such
        curitem = None
        for item in self.children:
            item.selected = False

            if item.match_url(request):
                if curitem is None or len(curitem.url) < len(item.url):
                    curitem = item

        if curitem is not None:
            curitem.selected = True

    def match_url(self, request):
        return self.url_name == request.resolver_match.url_name

        # """
        # match url determines if this is selected
        # """
        # matched = False
        # if self.exact_url:
        #     if re.match("%s$" % (self.url,), request.path):
        #         matched = True
        # elif re.match("%s" % self.url, request.path):
        #     matched = True
        # return matched


def menu_combo(views=(), menu='main', title='Menu Title', icon='mdi mdi-menu', create_link=False):

    children = []
    for view in views:
        if isinstance(view, list):
            children += view
        else:
            children += view().load_menus(create_link=create_link, get_children=True)

    if children or create_link:
        Menu.add_item(
            menu,
            MenuItem(title, None, no_link=True, icon=icon, children=children)
        )
