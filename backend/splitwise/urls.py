"""splitwise URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings

import splitwise.apps.users.views as user_views
import splitwise.apps.expenses.views as expense_views

router = routers.DefaultRouter()
router.get_api_root_view().cls.__name__ = "DongerAPIRoot"
router.get_api_root_view().cls.__doc__ = "Fully browsable back-end API of the Donger platform"

router.register('user', user_views.UserViewSet, basename='user')
router.register('friend', user_views.FriendViewSet, basename='friend')
router.register('clique', user_views.CliqueViewSet, basename='clique')
router.register('expense', expense_views.ExpenseViewSet, basename='expense')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
