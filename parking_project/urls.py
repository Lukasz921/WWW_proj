from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from parking import views
from rest_framework.routers import DefaultRouter

# Router API
router = DefaultRouter()
router.register(r'spots', views.ParkingSpotViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core URLs
    path('', views.home, name='home'),
    path('zone/<int:zone_id>/', views.zone_detail, name='zone_detail'),
    
    # Data & Forms URLs
    path('my-reservations/', views.reservation_list, name='reservation_list'),
    path('reserve/', views.create_reservation, name='create_reservation'),
    path('reserve/edit/<int:pk>/', views.edit_reservation, name='edit_reservation'),
    
    # Auth URLs (Django wbudowane + rejestracja)
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    
    # Password Reset (Wymóg: "fałszywy" mechanizm)
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # API URLs
    path('api/', include(router.urls)),
]