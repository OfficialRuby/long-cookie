from django.urls import path
from reward.views import (IndexView, EarnRewardView, SupplyParameterView,
                          ConnectDeviceView, connect_device, disconnect_device, ConnectAppView, connect_app,
                          disconnect_app, verify_app_token, HomeView)

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('dashboard/', IndexView.as_view(), name='home'),
    path('earn-reward/', EarnRewardView.as_view(), name='earn_reward'),
    path('supply-parameters/', SupplyParameterView.as_view(), name='supply_param'),
    path('connect-devices/', ConnectDeviceView.as_view(), name='connect_device'),
    path('connect-apps/', ConnectAppView.as_view(), name='connect_app'),
    path('app/connection-response/', verify_app_token, name='connection_response'),
    path('connect-device/<int:id>/', connect_device, name='connect_one_device'),
    path('disconnect-device/<int:id>/', disconnect_device, name='disconnect_one_device'),
    path('connect-app/<int:id>/', connect_app, name='connect_one_app'),
    path('disconnect-app/<int:id>/', disconnect_app, name='disconnect_one_app'),

]
