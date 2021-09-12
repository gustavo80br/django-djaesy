from django.utils.translation import gettext_lazy as _


permission_groups = [
    {
        'label': _('Usuários'),
        'permissions': (
            ('djaesy.user.add_user', _('Adicionar')),
            ('djaesy.user.change_user', _('Editar')),
            ('djaesy.user.delete_user', _('Remover')),
            ('djaesy.user.view_user', _('Visualizar')),
            ('djaesy.user.export', _('Exportar')),
        )
    },
    {
        'label': _('Perfís de Usuários'),
        'permissions': (
            ('djaesy.role.add_role', _('Adicionar')),
            ('djaesy.role.change_role', _('Editar')),
            ('djaesy.role.delete_role', _('Remover')),
            ('djaesy.role.view_role', _('Visualizar')),
            ('djaesy.role.export', _('Exportar')),
        )
    },
]



