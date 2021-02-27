from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('expense/new/', views.add_expense, name='expense-create'),
    path('expense/<int:pk>/update/', views.update_expense, name='expense-update'),
    path('expense/<int:pk>/delete/confirm/', views.confirm_delete_expense, name='expense-confirm-delete'),
    path('expense/<int:pk>/delete/', views.delete_expense, name='expense-delete'),
    path('api/expenses/', api_views.expense_list),
    path('api/expenses/<int:pk>', api_views.expense_detail),
]
