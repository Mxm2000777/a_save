from django.urls import path, re_path
#from .views import login_page, reg_page, index, profile, logout_page, create_order, orders, clicker, changeprofile, order, chat, create_blank
                    #ссылка, func
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns = [path('reg', views.reg_page), 
               path('login', views.login_page), 
               path('base', views.index),
               path("logout", views.logout_page)
]