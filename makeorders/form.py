from django import forms
from django.forms.forms import Form
from .models import Clients, Consignees, Orders, Sentorder

class Clientform(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['party', 'address',]
        widgets = {'party':forms.TextInput(attrs={'class':'form-control'}),
        'address':forms.TextInput(attrs={'class':'form-control'}),
        }



class consigneeform(forms.ModelForm):
    class Meta:
        model = Consignees
        fields = ['consignee', 'station', 'trasport',]
        labels={'consignee':'Consignee',}
        widgets = {'consignee':forms.TextInput(attrs={'class':'form-control'}),                      
                 'station':forms.TextInput(attrs={'class':'form-control'}),        
                   'trasport':forms.TextInput(attrs={'class':'form-control'}),}
                


class ordesform(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['orderdate','item_name','ordered_cartons']
        widgets ={'orderdate':forms.DateInput(attrs={'class':'form-control','type':'Date'}),
            'item_name':forms.TextInput(attrs={'class':'form-control'}),
            'ordered_cartons':forms.TextInput(attrs={'class':'form-control','type':'integer'}),            
        }


class Sentorderform(forms.ModelForm):
    class Meta:
        model = Sentorder
        fields=['date','cartons','status','by',]        
        widgets = {'date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        'cartons':forms.TextInput(attrs={'class':'form-control','type':'integer'}),
        'status':forms.Select(attrs={'class':'form-select'}),
        'by':forms.Select(attrs={'class':'form-select'}),
        }
       