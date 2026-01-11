from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from parking import views
from rest_framework.routers import DefaultRouter

# Użytkownik wpisuje adres strony, wówczas trafia to tutaj
# Filtrujemy po adresach i jeżeli taki istnieje, zwracamy odpowiednie view

# Router API - tworzymy automatyczne urle dla spots i reservations
router = DefaultRouter()
router.register(r'spots', views.ParkingSpotViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('zone/<int:zone_id>/', views.zone_detail, name='zone_detail'),
    path('my-reservations/', views.reservation_list, name='reservation_list'),
    path('reserve/', views.create_reservation, name='create_reservation'),
    path('reserve/edit/<int:pk>/', views.edit_reservation, name='edit_reservation'),
    path('reserve/delete/<int:pk>/', views.delete_reservation, name='delete_reservation'),

    # Auth URLs - Django wbudowane + rejestracja
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    
    # Password Reset
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # API
    path('api/', include(router.urls)), # podpinamy te router API tutaj pod prefiksem /api
]