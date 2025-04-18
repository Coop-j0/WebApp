from django.urls import path
from . import views

urlpatterns = [
    path('make_payment/', views.make_payment, name='make_payment'),
    path('send_request/', views.send_request, name='send_request'),
    path('pending_requests/', views.pending_requests, name='pending_requests'),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('decline-request/<int:request_id>/', views.decline_request, name='decline_request'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_view_users/', views.admin_view_users, name = 'admin_view_users'),
    path('admin_view_transactions/', views.admin_view_transactions, name = 'admin_view_transactions'),
    path('register_admin/', views.register_admin, name = 'register_admin'),
    path('transaction_history/', views.transaction_history, name = 'transaction_history'),
    path('api/convert/', views.currency_conversion_api, name='currency_conversion_api'),
]