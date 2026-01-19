from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Strona główna + strefy
    path('', views.home, name='home'),
    path('zone/<int:zone_id>/', views.zone_detail, name='zone_detail'),
    # Rezerwacje
    path('my-reservations/', views.reservation_list, name='reservation_list'),
    path('reserve/', views.create_reservation, name='create_reservation'),
    path('reserve/edit/<int:pk>/', views.edit_reservation, name='edit_reservation'),
    path('reserve/delete/<int:pk>/', views.delete_reservation, name='delete_reservation'),
    # Logowanie + rejestracja
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    # Reset hasła
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]