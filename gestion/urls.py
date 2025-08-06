from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('actas/<int:id>/', views.acta),
    path('actas/', views.actas_list),
    path('gestiones/', views.crear_gestion),
]