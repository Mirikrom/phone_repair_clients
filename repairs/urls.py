from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'repairs'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', RedirectView.as_view(url='/', permanent=False)),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('buyurtmalar/', views.order_list, name='order_list'),
    path('tayyor/', views.ready_phones_list, name='ready_phones_list'),
    path('zapchast/', views.zapchast_zakaz_list, name='zapchast_zakaz_list'),
    path('zapchast/add/', views.zapchast_add, name='zapchast_add'),
    path('zapchast/<int:pk>/toggle/', views.zapchast_toggle, name='zapchast_toggle'),
    path('zapchast/olindi/', views.zapchast_mark_done, name='zapchast_mark_done'),
    path('zapchast/tugatish/', views.zapchast_tugatish, name='zapchast_tugatish'),
    path('zapchast/<int:pk>/edit/', views.zapchast_edit, name='zapchast_edit'),
    path('zapchast/<int:pk>/delete/', views.zapchast_delete, name='zapchast_delete'),
    path('zapchast/print/', views.zapchast_print, name='zapchast_print'),
    path('zapchast/image/', views.zapchast_image, name='zapchast_image'),
    path('vizitka/', views.vizitka_choice, name='vizitka_choice'),
    path('vizitka/print/', views.vizitka_print, name='vizitka_print'),
    path('vizitka/carta/', views.carta_nomer_print, name='carta_nomer_print'),
    path('istoriya/', views.order_history, name='order_history'),
    path('qarzdorlar/', views.debtors_list, name='debtors_list'),
    path('api/autocomplete/', views.autocomplete, name='autocomplete'),
    path('api/reminders/due/', views.reminders_due, name='reminders_due'),
    path('api/reminders/ack/', views.reminders_ack, name='reminders_ack'),
    path('add/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/print/', views.order_print, name='order_print'),
    path('<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('<int:pk>/tugatish/', views.order_mark_ready, name='order_mark_ready'),
    path('<int:pk>/olib-ketildi/', views.order_mark_completed, name='order_mark_completed'),
]
