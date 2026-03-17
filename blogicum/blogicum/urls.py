"""blogicum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import include, path, reverse_lazy


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
handler403csrf = 'pages.views.csrf_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Логин.
    path('auth/login/', views.LoginView.as_view(), name='login'), 
    # Логаут.
    path('auth/logout/', views.LogoutView.as_view(), name='logout'), 
    # Изменение пароля.
    path('auth/password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # Сообщение об успешном изменении пароля.
    path('auth/password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # Восстановление пароля.
    path('auth/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # Сообщение об отправке ссылки для восстановления пароля.
    path('auth/password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # Вход по ссылке для восстановления пароля.
    path('auth/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Сообщение об успешном восстановлении пароля.
    path('auth/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('auth/', include('django.contrib.auth.urls')), 
    path(
        'auth/registration/', 
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
