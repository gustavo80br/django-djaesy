from django.shortcuts import render

from djaesy.core.views.base import BaseView


class DjaesyTabViewWrapper(BaseView):

    def get(self, request, *args, **kwargs):
        context = self._get_render_context()
        context['tab_url'] = f'/{kwargs.get("path", "")}'
        return render(request, 'djaesy/base2.html', context=context)