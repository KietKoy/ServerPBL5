from django.urls import path
from api import views

urlpatterns = [
    path('tickets/', views.tickets_list),
    path('tickets/create/', views.create_ticket),
    path('tickets/get/<str:license_plate>/', views.get_ticket),
    path('tickets/update/<str:ticket_id>/', views.update_ticket),
    
    path('accounts/', views.accounts_list),
    path('accounts/update/<int:account_id>/', views.update_password),

    path('parkinglots/', views.parkinglots_list),
    path('parkinglots/update/<int:parkinglot_id>/', views.update_status),

]
