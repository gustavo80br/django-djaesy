from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.safestring import SafeString
from django.views.generic.base import View

from djaesy.base_views import BaseView, CrudCombo, TableListView
# from djaesy.mongo import Mongo
from sandbox.models import TabB, TabA


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': "event_notifications"
    })


@method_decorator(login_required, name='dispatch')
class SandboxView(BaseView):

    template_name = 'sandbox/sandbox.html'
    content_title = 'Sandbox'

    # Sidebar
    option_menubar_open = False
    option_menubar_toggle = True
    # Fullscreen
    option_in_fullscreen = False
    option_fullscreen_toggle = True
    # Control sidebar
    option_sidebar = False
    option_sidebar_open = False
    option_sidebar_toggle = False
    option_sidebar_size = '240px'
    # Footer
    option_footer = False

    def _get_render_context(self):
        ctx = super()._get_render_context()
        ctx.update(self.sandbox_function())
        return ctx

    # ------ SANDBOX COMEÇA AQUI -------

    @staticmethod
    def sandbox_function():

        # import pandas as pd
        #
        # mongodb = Mongo.get_db()
        #
        # ultimo_proc = mongodb['ultimo_proc']
        #
        # consulta_ultimo_proc = ultimo_proc.find({})
        #
        # df = pd.DataFrame(consulta_ultimo_proc)
        #
        # var_a = 187
        # var_b = 'Testando 123'
        # dataframe_em_html = df.to_html()
        #
        # resposta = {
        #     'variavel_a': var_a,
        #     'variavel_b': var_b,
        #     'dataframe': SafeString(dataframe_em_html)
        # }
        #
        # return resposta
        return None


class RodrigoView(View):

    def get(self, request):
        return HttpResponse('TESTE')


class TabBView(CrudCombo):

    model = TabB
    permission = ''

    icon = 'mdi mdi-google-circles-group'

    class List(TableListView):
        table_columns = ['name', 'description', 'relationship__name']


class TabAView(CrudCombo):

    model = TabA

    icon = 'mdi mdi-google-circles-group'

    class List(TableListView):
        table_columns = ['name']
