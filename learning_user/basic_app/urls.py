from django.conf.urls import url
from basic_app import views

app_name='basic_app'

urlpatterns = [
    url(r'registration/$',views.user_registration,name='registration'),
    url(r'login/',views.user_login,name='login'),
    url(r'logout/',views.user_logout,name='logout'),
]
