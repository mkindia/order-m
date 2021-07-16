"""orders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from . import views

urlpatterns = [
    path('userlogin/',views.user_login,name="user_login"),
    path('userlogout/',views.user_logout,name="user_logout"),
    path('', views.home, name='home'),
    path('for_data/',views.for_data, name='for_data'),
    path('addconsignee/<pr>/',views.add_consignee, name='add_consignee'),
    path('editconsignee/<atri>/',views.edit_consignee, name='edit_consignee'),
    path('consigneedetails/',views.consigneeDetails,name='consigneedetails'),    
    path('con_data/<atri>/',views.con_id, name='con_id'),
    path('addorder/<atri>/',views.add_order, name='addorder'),
    path('addsent/<atri>/',views.addsent, name='addsent'),
    path('sent_data/',views.sent_data, name='sent_data'),
    path('items/<atri>/',views.items, name='items'),
    path('items_data/',views.items_data, name='items_data'), 
    path('addparty/<pr>/',views.add_party, name='addparty'),
    path('editparty/<atri>/',views.edit_party, name='edit_party'),
    path('form_data/<atri>',views.form_data, name='form_data'),
    path('itemwiseorders/<filter>/',views.item_wise, name='item_wise'),
    path('itemwise_data/<filter>/',views.itemwise_data, name='itemwise_data'),
    
   
    
   


]
