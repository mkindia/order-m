from django import forms
from django.contrib.auth import authenticate
from django.forms import fields, widgets
from django.forms.fields import Field
from django.forms.forms import Form
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.forms import AuthenticationForm
from .models import Clients, Consignees, Orders, Sentorder, Items
from makeorders import models

class Itemsform(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['item_name']
        labels={'item_name':'Item Name',}
        widgets = {'item_name':forms.TextInput(attrs={'class':'form-control text-capitalize'})}


class Userauthform(AuthenticationForm):
         fields=['first_name']
         username=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
         password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class Clientform(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['party', 'station', 'transport']
        widgets = {'party':forms.TextInput(attrs={'class':'form-control text-capitalize'}),
        'station':forms.TextInput(attrs={'class':'form-control text-capitalize'}),
        'transport':forms.TextInput(attrs={'class':'form-control text-capitalize'}),
        }
       


class consigneeform(forms.ModelForm):
    class Meta:
        model = Consignees
        fields = ['consignee', 'station', 'transport',]       
        widgets = {'consignee':forms.TextInput(attrs={'class':'form-control text-capitalize'}),                      
                 'station':forms.TextInput(attrs={'class':'form-control text-capitalize'}),        
                   'transport':forms.TextInput(attrs={'class':'form-control text-capitalize'}),}
                
class ordesform(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['orderdate','item_price','qty','unit']
        labels={'qty':'Qty'}
        widgets ={'orderdate':forms.DateInput(attrs={'class':'form-control','type':'Date'}),
            'item_price':forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.01'}),           
            'qty':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'unit':forms.Select(attrs={'class':'form-select'}),           
        }


class Sentorderform(forms.ModelForm):
    class Meta:
        model = Sentorder
        fields=['date','qty','status','consignee_id','by',] 
        labels={'qty':'Qty'}       
        widgets = {'date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        'qty':forms.TextInput(attrs={'class':'form-control','type':'number'}),
        'status':forms.Select(attrs={'class':'form-select'}),
        'consignee_id':forms.Select(attrs={'class':'form-select'}),
        'by':forms.Select(attrs={'class':'form-select'}),
        }
       