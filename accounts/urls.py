from xml.etree.ElementInclude import include

from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts import views


router = DefaultRouter()
router.register(r'api/users', views.UserViewSet, basename='api-users')
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
] + router.urls