from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router API
router = DefaultRouter()
router.register(r'spots', views.ParkingSpotViewSet)
router.register(r'reservations', views.ReservationViewSet)

# Urle wciągnięte do głównego projektu
urlpatterns = [
    path('', include(router.urls)),
]