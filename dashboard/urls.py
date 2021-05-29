from django.urls import path 
from dashboard import views

urlpatterns = [  
    path('volunteer/',views.vhome,name='vhome'),
    path('user/',views.uhome,name= 'uhome'),
    path('acceptRequest/<int:pk>/',views.acceptRequest,name='acceptRequest'),
    path('createRequest/<int:pk>',views.createRequest,name='createRequest'),
    path('user/markDelivered/',views.markDelivered,name='markDelivered')

]