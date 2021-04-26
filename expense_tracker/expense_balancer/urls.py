from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='expense-balancer'),
    path('events/new', views.add_event, name='event-create'),
    path('events/<int:pk>/contributors/new', views.add_contributor, name='contributor-create'),
    path('events/<int:pk>/expenses/new', views.add_expense, name='expense-create'),
    path('expenses/<int:expense_pk>/contribution/new', views.add_contribution, name='contribution-create'),
]
