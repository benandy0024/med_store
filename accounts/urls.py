from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from.views import login_page,register_page
#guest_register_page
urlpatterns = [
    url('login', login_page,name='login'),
url('logout/', LogoutView.as_view(), name='logout'),
    url('register', register_page, name='register'),
    # url('register/guest', guest_register_page, name='guest_register'),

]