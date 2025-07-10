from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.main_view, name='main'), 
    path('expenses/', views.expense_view, name='expense_list'),
    path('expenses/delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    
    path('incomes/', views.income_view, name='income_list'),
    path('incomes/delete/<int:pk>/', views.delete_income, name='delete_income'),

]