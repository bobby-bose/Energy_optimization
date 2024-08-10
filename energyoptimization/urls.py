"""energyoptimization URL Configuration

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
from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('bathroom/create/', bathroom_create, name='bathroom_create'),
    path('kitchen-appliance/create/', kitchen_appliance_create, name='kitchen_appliance_create'),
    path('bedroom/create/', bedroom_appliance_create, name='bedroom_create'),
    path('dininghall/create/', dininghall_appliance, name='dininghall_create'),
    path('livingroom/create/', livingroom_appliance, name='livingroom_create'),
    path('random_forest/', random_forest, name='random_forest'),
    path('k_nearest_neighbours/', k_nearest_neighbours, name='k_nearest_neighbours'),
    path('linear_regression/', linear_regression, name='linear_regression'),
    path('svm/', svm, name='svm'),
    path('bathroom/list/', bathroom_list, name='bathroom_list'),
    path('energy/consumption/', calculate_energy_consumption, name='calculate_energy_consumption'),
    path('kitchen/appliance/list/', kitchen_appliance_list, name='kitchen_appliance_list'),
    path('energy/consumption1/', calculate_energy_consumption1, name='calculate_energy_consumption1'),
    path('bedroom/appliance/list/',bedroom_appliance_list, name='bedroom_appliance_list'),
    path('energy/consumption2/', calculate_energy_consumption2, name='calculate_energy_consumption2'),
    path('dininghall/appliance/list/',dininghall_appliance_list, name='dininghall_appliance_list'),
    path('energy/consumption3/', calculate_energy_consumption3, name='calculate_energy_consumption3'),
    path('livingroom/appliance/list/',livingroom_appliance_list, name='livingroom_appliance_list'),
    path('energy/consumption4/', calculate_energy_consumption4, name='calculate_energy_consumption4'),
    path('',index,name='index'),
    path('logout/', logout_view, name='logout'),
    path('bathroom/<int:bathroom_id>/delete/', bathroom_delete, name='bathroom_delete'),
    path('bedroom/<int:bedroom_id>/delete/', bedroom_delete, name='bedroom_delete'),
    path('dininghall/<int:dininghall_id>/delete/', dininghall_delete, name='dininghall_delete'),
    path('kitchen/<int:kitchen_id>/delete/', kitchen_delete, name='kitchen_delete'),
    path('livingroom/<int:livingroom_id>/delete/', livingroom_delete, name='livingroom_delete'),
    path('bathroom/piechart/', piechart, name='piechart'),
    path('scatterplot/', scatterplot, name='scatterplot'),
    path('bedroom/piechart/', piechart1, name='piechart1'),
    path('kitchen/piechart/', piechart2, name='piechart2'),
    path('dininghall/piechart/', piechart3, name='piechart3'),
    path('livingroom/piechart/', piechart4, name='piechart4'),
    path('scatterplot1/', scatterplot1, name='scatterplot1'),
    path('scatterplot2/', scatterplot2, name='scatterplot2'),
    path('scatterplot3/', scatterplot3, name='scatterplot3'),
    path('scatterplot4/', scatterplot4, name='scatterplot4'),
    path('charts/',charts,name="charts"),
    path('january/',january,name="january"),
    path('february/',february,name="february"),
    path('march/',march,name="march"),
    path('april/',april,name="april"),
    path('may/',may,name="may"),
    path('june/',june,name="june"),
    path('july/',july,name="july"),
    path('august/',august,name="august"),
    path('september/',september,name="september"),
    path('october/',october,name="october"),
    path('november/',november,name="november"),
    path('december/',december,name="december"),
path('contact/', contact, name='contact'),
path('billings/', billings, name='billings'),



   





    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
