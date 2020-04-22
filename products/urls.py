from django.contrib import admin
from django.conf.urls import url,include
from.views import ProductListView,ProductDetailView,home

urlpatterns = [
    url('admin_panel/', admin.site.urls),
    url(r'^home$',home, name='home'),
    url(r'^$', ProductListView.as_view(), name='list'),
    url('(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail')
]