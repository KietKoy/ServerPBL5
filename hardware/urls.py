from django.urls import path
from hardware import views

urlpatterns = [
    path('create/', views.create_ticket),
    path('update/', views.update_ticket),
    path('detect/', views.run_detect),
    
]