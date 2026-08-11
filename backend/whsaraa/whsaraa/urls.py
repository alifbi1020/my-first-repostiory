"""
URL configuration for whsaraa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView
from venues.views import city_results, home, dashboard, vacancy_list, dashboard_view, dashboard_stats
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_view, logout_view
from reservations.views import create_reservation, get_reservation_detail, my_reservations_view, cancel_reservation

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('index.html', home),

    path('city.html', city_results, name='city_results'),
    path('api/vacancies/', vacancy_list, name='vacancy_list'),
    path('api/reservations/create/', create_reservation, name='create_reservation'),
    path('api/reservations/<int:reservation_id>/', get_reservation_detail, name='get_reservation_detail'),
    path('api/reservations/<int:reservation_id>/cancel/', cancel_reservation, name='cancel_reservation'),
    path('my-reservations/', my_reservations_view, name='my_reservations'),
    path('api/dashboard/stats/', dashboard_stats, name='dashboard_stats'),

    path('login.html', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard.html', dashboard_view, name='dashboard'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)