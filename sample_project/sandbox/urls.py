"""djaesy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

# from sandbox import api
from sandbox.views import SandboxView, RodrigoView, index, room, TabBView, TabAView

urlpatterns = [

    path('', include(TabBView().urls)),
    path('', include(TabAView().urls)),

    path('sandbox/', SandboxView.as_view(), name='sandbox_view'),
    path('rodrigo/', RodrigoView.as_view(), name='rodrigo_view'),

    # path('chat/', index, name='index'),
    # path('chat/<str:room_name>/', room, name='room'),

    # API
    # path('api/v1/update/tracker/<text>', api.UpdateTrackerStatus.as_view(), name='api_update_tracker'),

]
