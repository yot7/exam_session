from django.urls import path
from common.views import home_page

app_name = 'common'

urlpatterns = [
    path('', home_page, name='home'),
]