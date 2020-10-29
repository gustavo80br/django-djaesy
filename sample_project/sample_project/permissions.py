from django.utils.translation import ugettext_lazy as _

permission_groups = [
    # {
    #     'label': _('Usuários'),
    #     'permissions': (
    #         ('accounts.user.add_user', _('Adicionar')),
    #         ('accounts.user.change_user', _('Editar')),
    #         ('accounts.user.delete_user', _('Remover')),
    #         ('accounts.user.view_user', _('Visualizar')),
    #         ('accounts.user.export', _('Exportar')),
    #     )
    # },
    # {
    #     'label': _('Perfís de Usuários'),
    #     'permissions': (
    #         ('accounts.userprofile.add_userprofile', _('Adicionar')),
    #         ('accounts.userprofile.change_userprofile', _('Editar')),
    #         ('accounts.userprofile.delete_userprofile', _('Remover')),
    #         ('accounts.userprofile.view_userprofile', _('Visualizar')),
    #         ('accounts.userprofile.export', _('Exportar')),
    #     )
    # },
    # {
    #     'label': _('Veículos'),
    #     'permissions': (
    #         ('trackobj.vehicle.add_vehicle', _('Adicionar')),
    #         ('trackobj.vehicle.change_vehicle', _('Editar')),
    #         ('trackobj.vehicle.delete_vehicle', _('Remover')),
    #         ('trackobj.vehicle.view_vehicle', _('Visualizar')),
    #         ('trackobj.vehicle.export', _('Exportar'))
    #     )
    # },
    # {
    #     'label': _('Administrar Clientes'),
    #     'entities': [0],
    #     'permissions': (
    #         ('clients.client.add_client', _('Adicionar'), [0]),
    #         ('clients.client.change_client', _('Editar'), [0]),
    #         ('clients.client.delete_client', _('Remover'), [0]),
    #         ('clients.client.view_client', _('Visualizar'), [0]),
    #         ('clients.client.export', _('Exportar'), [0]),
    #     )
    # },
    # {
    #     'label': _('Clientes de Empresas'),
    #     'entities': [0, 1],
    #     'permissions': (
    #         ('clients.companyclient.add_companyclient', _('Adicionar'), [0, 1]),
    #         ('clients.companyclient.change_companyclient', _('Editar'), [0, 1]),
    #         ('clients.companyclient.delete_companyclient', _('Remover'), [0, 1]),
    #         ('clients.companyclient.view_companyclient', _('Visualizar'), [0, 1]),
    #         ('clients.companyclient.export', _('Exportar'), [0, 1])
    #     )
    # },
    # {
    #     'label': _('Clientes de Representates'),
    #     'entities': [0, 2],
    #     'permissions': (
    #         ('clients.representativeclient.add_representativeclient', _('Adicionar'), [0, 2]),
    #         ('clients.representativeclient.change_representativeclient', _('Editar'), [0, 2]),
    #         ('clients.representativeclient.delete_representativeclient', _('Remover'), [0, 2]),
    #         ('clients.representativeclient.view_representativeclient', _('Visualizar'), [0, 2]),
    #         ('clients.representativeclient.export', _('Exportar'), [0, 2]),
    #     )
    # },
    # {
    #     'label': _('Administrar Empresas'),
    #     'entities': [0],
    #     'permissions': (
    #         ('clients.company.add_company', _('Adicionar')),
    #         ('clients.company.change_company', _('Editar')),
    #         ('clients.company.delete_company', _('Remover')),
    #         ('clients.company.view_company', _('Visualizar')),
    #         ('clients.company.export', _('Exportar'))
    #     )
    # },
    # {
    #     'label': _('Administrar Representantes'),
    #     'entities': [0],
    #     'permissions': (
    #         ('clients.representative.add_representative', _('Adicionar')),
    #         ('clients.representative.change_representative', _('Editar')),
    #         ('clients.representative.delete_representative', _('Remover')),
    #         ('clients.representative.view_representative', _('Visualizar')),
    #         ('clients.representative.export', _('Exportar')),
    #     )
    # },
    # {
    #     'label': _('Representantes de Empresas'),
    #     'entities': [0, 1],
    #     'permissions': (
    #         ('clients.companyrepresentative.add_companyrepresentative', _('Adicionar')),
    #         ('clients.companyrepresentative.change_companyrepresentative', _('Editar')),
    #         ('clients.companyrepresentative.delete_companyrepresentative', _('Remover')),
    #         ('clients.companyrepresentative.view_companyrepresentative', _('Visualizar')),
    #         ('clients.companyrepresentative.export', _('Exportar'))
    #     )
    # },
    # {
    #     'label': _('Centro de Custo'),
    #     'entities': [0, 1, 2, 3],
    #     'permissions': (
    #         ('clients.costcenter.add_costcenter', _('Adicionar')),
    #         ('clients.costcenter.change_costcenter', _('Editar')),
    #         ('clients.costcenter.delete_costcenter', _('Remover')),
    #         ('clients.costcenter.view_costcenter', _('Visualizar')),
    #         ('clients.costcenter.export', _('Exportar'))
    #     )
    # },
    # {
    #     'label': _('Módulos'),
    #     'entities': [0, 1],
    #     'permissions': (
    #         ('trackers.tracker.add_tracker', _('Adicionar')),
    #         ('trackers.tracker.change_tracker', _('Editar')),
    #         ('trackers.tracker.delete_tracker', _('Remover')),
    #         ('trackers.tracker.view_tracker', _('Visualizar')),
    #         ('trackers.tracker.export', _('Exportar'))
    #     )
    # },
    # {
    #     'label': _('Tipo de Módulos'),
    #     'entities': [0],
    #     'permissions': (
    #         ('trackers.trackertype.add_trackertype', _('Adicionar'), [0]),
    #         ('trackers.trackertype.change_trackertype', _('Editar'), [0]),
    #         ('trackers.trackertype.delete_trackertype', _('Remover'), [0]),
    #         ('trackers.trackertype.view_trackertype', _('Visualizar'), [0]),
    #         ('trackers.trackertype.export', _('Exportar'), [0])
    #     )
    # },
    # {
    #     'label': _('Fabricantes de Módulo'),
    #     'entities': [0],
    #     'permissions': (
    #         ('trackers.trackermanufacturer.add_trackermanufacturer', _('Adicionar')),
    #         ('trackers.trackermanufacturer.change_trackermanufacturer', _('Editar')),
    #         ('trackers.trackermanufacturer.delete_trackermanufacturer', _('Remover')),
    #         ('trackers.trackermanufacturer.view_trackermanufacturer', _('Visualizar')),
    #         ('trackers.trackermanufacturer.export', _('Exportar'))
    #     )
    # },
    # {
    #     'label': _('Modelos de Módulo'),
    #     'entities': [0],
    #     'permissions': (
    #         ('trackers.trackermodel.add_trackermodel', _('Adicionar')),
    #         ('trackers.trackermanufacturer.change_trackermodel', _('Editar')),
    #         ('trackers.trackermodel.delete_trackermodel', _('Remover')),
    #         ('trackers.trackermodel.view_trackermodel', _('Visualizar')),
    #         ('trackers.trackermodel.export', _('Exportar'))
    #     )
    # },
    # {
    #     'label': _('Alertas'),
    #     'permissions': (
    #         ('alerts.alert.add_alert', _('Adicionar')),
    #         ('alerts.alert.change_alert', _('Editar')),
    #         ('alerts.alert.delete_alert', _('Remover')),
    #         ('alerts.alert.view_alert', _('Visualizar')),
    #         ('alerts.alert.export', _('Exportar'))
    #     )
    # },
    # {
    #     "label": _('Cercas'),
    #     "permissions": [
    #         ("alerts.henge.add_henge", _("Criar")),
    #         ("alerts.henge.change_henge", _("Editar")),
    #         ("alerts.henge.delete_henge", _("Remover")),
    #         ("alerts.henge.view_henge", _("Visualizar")),
    #         ("alerts.henge.export", _('Exportar')),
    #     ]
    # },
    # {
    #     "label": _('Notificações'),
    #     "permissions": [
    #         ("alerts.notification.add_notification", _("Criar")),
    #         ("alerts.notification.change_notification", _("Editar")),
    #         ("alerts.notification.delete_notification", _("Remover")),
    #         ("alerts.notification.view_notification", _("Visualizar")),
    #         ("alerts.henge.export", _('Exportar')),
    #     ]
    # },
    # {
    #     'label': _('Monitoramento'),
    #     'permissions': (
    #         ('trackers.tracker.view_monitoring_map', _('Mapa de monitoramento')),
    #         ('trackers.tracker.view_monitoring_table', _('Tabela de monitoramento'))
    #     )
    # },
    # {
    #     "label": _('Plano de Manutenção'),
    #     "permissions": [
    #         ("maintenance.maintenanceplan.add_maintenanceplan", _("Criar")),
    #         ("maintenance.maintenanceplan.change_maintenanceplan", _("Editar")),
    #         ("maintenance.maintenanceplan.delete_maintenanceplan", _("Remover")),
    #         ("maintenance.maintenanceplan.view_maintenanceplan", _("Visualizar")),
    #     ]
    # },
    # {
    #     "label": _('Items de Manutenção'),
    #     "permissions": [
    #         ("maintenance.maintenanceitem.add_maintenanceitem", _("Criar")),
    #         ("maintenance.maintenanceitem.change_maintenanceitem", _("Editar")),
    #         ("maintenance.maintenanceitem.delete_maintenanceitem", _("Remover")),
    #         ("maintenance.maintenanceitem.view_maintenanceitem", _("Visualizar")),
    #     ]
    # },
    # {
    #     "label":  _('Relatórios'),
    #     "permissions": [
    #         ("reports.generatedreport.work_report_generate", _("Horas Trabalhadas")),
    #         # ("reports.generatedreport.change_generatedreport", _("Alterar")),
    #         # ("reports.generatedreport.delete_generatedreport", _("Remover generated report")),
    #         # ("reports.generatedreport.view_generatedreport", _("Visualizar generated report"))
    #     ]
    # },
    # {
    #     "label":  _('Motoristas'),
    #     "permissions": [
    #         ("drivers.driver.add_driver", _("Criar")),
    #         ("drivers.driver.change_driver", _("Editar")),
    #         ("drivers.driver.delete_driver", _("Remover")),
    #         ("drivers.driver.view_driver", _("Visualizar"))
    #     ]
    # },
]



