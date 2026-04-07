from django.urls import path
from common.views import home_page, async_dashboard_stats

app_name = 'common'

urlpatterns = [
    path('', home_page, name='home'),
    path('dashboard/', async_dashboard_stats, name='dashboard'),
]