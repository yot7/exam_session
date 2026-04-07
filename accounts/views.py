from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from accounts.forms import RegistrationForm
from accounts.serializers import UserSerializer

# Create your views here.
UserModel = get_user_model()

class RegisterView(UserPassesTestMixin, CreateView):
    form_class = RegistrationForm
    model = UserModel
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('common:home')

    def test_func(self):
        return not self.request.user.is_authenticated


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('common:home')


class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all().prefetch_related('groups')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']