import importlib
import json
from importlib import import_module
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from djaesy.models import CustomPermission

permissions = [] #import_module(settings.DJAESY_PERMISSIONS)

for app in settings.INSTALLED_APPS:
    try:
        app_permissions = importlib.import_module(f'{app}.permissions')
        permissions += app_permissions.permission_groups
    except:
        pass

PERMISSION_CACHE = {}


def get_permission(permission_type, model=None, permissions_by_model=None):
    """
    :param <str> permission_type:
    :param <Class> model:
    :param <Permission> permissions_by_model:
    :return <Permission, QuerySet>: Specific permission and all permission for the model passed
    """

    if model:
        cache_key = f'{str(permission_type)}_{str(model.__name__.lower())}'
    else:
        cache_key = permission_type

    permission, permission_by_model = PERMISSION_CACHE.get(cache_key, (None, None))

    if permission:
        return permission, permissions_by_model
    else:

        if not permissions_by_model:
            if not model:
                return '', Permission.objects.none()

            content_type = ContentType.objects.get_for_model(model)
            permissions_by_model = Permission.objects.filter(content_type=content_type).select_related()

        try:
            permission = permissions_by_model.filter(codename__startswith=permission_type).select_related().first()
            permission = f'{permission.content_type.app_label}.{permission.codename}'
            PERMISSION_CACHE[cache_key] = (permission, permission_by_model)
            return permission, permissions_by_model
        except Permission.DoesNotExist:
            return None, None
        except AttributeError:
            return None, None
        except Exception as e:
            raise Exception(f'get_permission: {e}')


def check_permissions():
    all_permissions = Permission.objects.all()
    check_delete_permission(all_permissions)
    check_create_permission(all_permissions)


def permission_tuple(permission_key, app_label=False):
    perm_key = permission_key.split('.')
    app_label_data = perm_key[0]
    model_name = perm_key[1]
    codename = perm_key[2]
    if not app_label:
        return model_name, codename
    else:
        return app_label_data, model_name, codename


def check_delete_permission(all_permissions):

    models_codename_permissions = list(
        all_permissions.values_list(
            'content_type__model', 'codename', 'custompermission', 'content_type__app_label'
        ).distinct()
    )

    tuple_permissions = get_tuple_permissions()

    for item in models_codename_permissions:
        model_name = item[0]
        codename = item[1]
        custom_permission = item[2]
        app_label = item[3]
        if custom_permission:
            if (model_name, codename) not in tuple_permissions:
                ct = ContentType.objects.get_for_model(apps.get_model(app_label=app_label, model_name=model_name))
                permission = all_permissions.get(codename=codename, content_type=ct)
                if hasattr(permission, 'custompermission'):
                    permission.delete()


def check_create_permission(all_permissions):
    try:
        models_codename_permissions = list(
            all_permissions.values_list('content_type__app_label', 'content_type__model', 'codename').distinct()
        )
        for group in permissions:
            for item in group['permissions']:
                permission_key = item[0]
                app_label, model_name, codename = permission_tuple(permission_key, app_label=True)
                if (app_label, model_name, codename) not in models_codename_permissions:
                    ct = ContentType.objects.get_for_model(apps.get_model(app_label=app_label, model_name=model_name))
                    permission_name = get_permission_name_by_key(permission_key)
                    CustomPermission.objects.create(
                        name=permission_name, codename=codename, content_type=ct
                    )
    except Exception as e:
        raise Exception(f'djaesy.utils.check_create_permission: {e}')


def get_permission_name_by_key(key):
    for group in permissions:
        for item in group['permissions']:
            permission_key = item[0]
            if permission_key == key:
                return item[1]
    return None


def get_tuple_permissions():
    tuple_permissions = []
    for group in permissions:
        for item in group['permissions']:
            tuple_permissions.append(permission_tuple(item[0]))
    return tuple_permissions


def build_all_permissions():

    path = Path(permissions.__file__)
    path = Path(path.parents[0], 'all_permissions.py')

    with open(path, 'w') as fp:

        data = {}

        exclude_L1 = ['sessions', 'easy_thumbnails', 'contenttypes', 'cities', 'auth', 'admin', 'djaesy']
        exclude_L2 = ['']

        for p in Permission.objects.all():
            if p.content_type.app_label not in exclude_L1:
                key = f'{p.content_type.app_label}_group'
                if key not in data:
                    data[key] = {
                        'label': p.content_type.app_label,
                        'permissions': []
                    }
                data[key]['permissions'].append((f'{p.content_type.app_label}.{p.content_type.model}.{p.codename}', p.name))
        data_str = json.dumps(data, indent=4)
        fp.write('all_permissions = ' + data_str)





