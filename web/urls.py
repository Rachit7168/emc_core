from django.urls import path
from . import views

urlpatterns = [
    # 1. Consumer Pages
    path('', views.index, name='index'),
    path('experience/<str:brand_key>/', views.experience, name='experience'),
    path('book/', views.book_table, name='book_table'),
    
    # 2. APIs (For Data Transfer)
    path('api/book/', views.api_book_table, name='api_book_table'),

    # 3. Dashboard Pages (Admin)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/bookings/', views.dashboard_bookings, name='dashboard_bookings'),
    path('dashboard/menu/', views.dashboard_menu, name='dashboard_menu'),
    path('dashboard/tables/', views.dashboard_tables, name='dashboard_tables'),
    
    # 4. Action URLs
    path('dashboard/menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('dashboard/menu/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),

    # 5. Setup URL
    path('setup-secret-key/', views.setup_data, name='setup_data'),
]