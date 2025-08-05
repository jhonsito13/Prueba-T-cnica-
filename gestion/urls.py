from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('actas/<int:id>/', views.acta),
    path('gestiones/', views.crear_gestion),
]