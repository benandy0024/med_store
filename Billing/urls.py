from django.contrib import admin
from django.conf.urls import url
from.views import payment_method_create_view,payment_method_view

urlpatterns = [
url('payment_method', payment_method_view, name='payment_method_view'),
url('payment_method/create', payment_method_create_view, name='payment_method_view_endpoint'),

]