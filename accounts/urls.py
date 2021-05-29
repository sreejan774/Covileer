from django.urls import path 
from accounts import views

urlpatterns = [ 
    path('signup/',views.signup,name = "signup"),
    path('login/',views.login,name = "login"),
    path('logout/',views.logout,name = "logout"),
    path('updateprofile/<int:pk>',views.updateprofile,name="updateprofile"),
    path('',views.home,name="home")
]