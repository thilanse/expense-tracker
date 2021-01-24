from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='tracker-home'),
  path('expense/<int:pk>/update/', views.update_expense, name='expense-update'),
  path('expense/<int:pk>/delete/confirm/', views.confirm_delete_expense, name='expense-confirm-delete'),
  path('expense/<int:pk>/delete/', views.delete_expense, name='expense-delete')
]