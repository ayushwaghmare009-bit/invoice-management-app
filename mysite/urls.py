from django.contrib import admin
from django.urls import path
from invoice_app import views
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RedirectView.as_view(url='/home/')),
    path('admin/', admin.site.urls),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('invoices/', views.invoices_list_view, name='invoices'),
    path('invoice/add/', views.add_invoice, name='add_invoice'),
    path('invoice/<int:pk>/edit/', views.edit_invoice, name='edit_invoice'),
    path('invoice/<int:pk>/delete/', views.delete_invoice, name='delete_invoice'),
    path('Login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('Logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', views.register_view, name='register'),
    path('invoice/<int:pk>/pdf/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
]
