from django.urls import path
from afs import views

app_name = 'afs'
urlpatterns = [
    path('', views.CalculatorView.as_view(), name='calculator'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('login', views.LoginView.as_view(), name='login'),
    path('delete_calculation/<int:calculation_id>', views.DeleteCalculationView.as_view(), name='delete_calculation'),
]
