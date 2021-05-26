from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='expense-balancer'),
    path('events/new', views.add_event, name='event-create'),
    path('events/<int:pk>/contributors/new', views.add_contributor, name='contributor-create'),
    path('events/<int:pk>/expenses/new', views.add_expense, name='expense-create'),
    path('events/<int:pk>/delete', views.delete_event, name='event-delete'),
    path('events/<int:pk>/delete-confirmation', views.delete_event_confirmation, name='event-delete-confirmation'),
    path('expenses/<int:pk>/contribution/new', views.add_contribution, name='contribution-create'),
    path('expenses/<int:pk>/delete', views.delete_expense, name='event-expense-delete'),
    path('expenses/<int:pk>/delete-confirmation', views.delete_expense_confirmation,
         name='event-expense-delete-confirmation'),
]
