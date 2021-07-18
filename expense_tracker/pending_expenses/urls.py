from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='pending-expenses'),
    path('new/', views.add_pending_expense, name='pending-expense-create'),
    path('complete/<int:pk>', views.complete, name='pending-expense-complete'),
    path('undo/<int:pk>', views.undo, name='pending-expenses-undo'),
]
