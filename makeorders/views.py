from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Clients, Consignees, Orders, Sentorder
from .form import consigneeform, ordesform, Sentorderform, Clientform, Userauthform
from makeorders import form

#User Login form
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=Userauthform(request=request, data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                vuser=authenticate(username=uname, password=upass)
                if vuser is not None:
                    login(request, vuser)
                    #messages.success(request,'Success')
                    return HttpResponseRedirect('/')

        else:        
            fm=Userauthform()
        return render(request,'userlogin.html',{'form':fm})
    else:
        return HttpResponseRedirect('/')    

#Logout user
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/userlogin/')   

# Create your views here.
def home(request):      
  if request.user.is_authenticated:
    con = Consignees.objects.all()    
    party=Clients.objects.all()
    sentdatails=Sentorder.objects.all()    
    if request.method == 'POST':
         clientform=Clientform(request.POST)
         sentorder_form=Sentorderform(request.POST)
         if clientform.is_valid():
             name=clientform.cleaned_data['party']
             address=clientform.cleaned_data['address']
             sev=Clients(party=name,address=address)
             sev.save()        
    
    else:
        clientform=Clientform()
        sentorder_form=consigneeform()

    return render(request, "index.html", {'cons': con, 'partys':party,'sent_details':sentdatails,
    'clientform':clientform, 'sentorder_form':sentorder_form, 'username':request.user,})
  else:
    return HttpResponseRedirect('/userlogin/')

def con_id(request):
    
    id = request.GET.get('cons1')   
    global Party_id
    Party_id=id
   
    cons1 = Consignees.objects.filter(party_id=id)    
    return render(request, 'con_data.html', {'consi' : cons1,})   
    #return render(request, '', {'consi' : cons1,}) 


def add_consignee(request):    
    if request.method == 'POST':        
        
        confom=consigneeform(request.POST)           
        if confom.is_valid(): 
                sht=confom.cleaned_data['consignee']
                sta=confom.cleaned_data['station']           
                tr=confom.cleaned_data['trasport']
                sev=Consignees(party_id=request.POST.get('party_id'), consignee=sht, station=sta, trasport=tr)
                sev.save()
                return HttpResponseRedirect('/')        
    
    else:
     party=Clients.objects.all()       
     confom=consigneeform()
    #print(id) 
    return render(request, 'add_consignee.html', {'form':confom,'partys':party})  

def edit_consignee(request):

    if request.method == 'POST': 

        confom=consigneeform(request.POST)
        if confom.is_valid():
                pi=Consignees.objects.get(pk=Consignee_id)
                pid= int(pi.party_id)
                sht=confom.cleaned_data['consignee']
                sta=confom.cleaned_data['station']           
                tr=confom.cleaned_data['trasport']
                sev=Consignees(id=Consignee_id,party_id=pid, consignee=sht, station=sta, trasport=tr)
                sev.save()   
                                 
                return HttpResponseRedirect('/')
    else:
        con=Consignees.objects.get(pk=Consignee_id)          
        conform=consigneeform(instance=con)        
        #conform=consigneeform()
    return render(request,'editconsignee.html', {'editform':conform})

   
def order_data(request):
    global Consignee_id
    if request.GET.get('conid'):       
        Consignee_id=request.GET.get('conid')
            
        orders = Orders.objects.filter(consignees_id=Consignee_id) 
    
    return render(request, 'for_data.html', {'order' : orders,})



def add_order(request):
      
   if request.method =='POST':
       ordfom=ordesform(request.POST)
       if ordfom.is_valid():
           date=ordfom.cleaned_data['orderdate']
           item_name=ordfom.cleaned_data['item_name']
           item_price=ordfom.cleaned_data['item_price']
           cartons=ordfom.cleaned_data['ordered_cartons']           
           sev=Orders(consignees_id=request.POST.get('consignee_id'),orderdate=date,
           item_name=item_name,item_price=item_price,ordered_cartons=cartons,balance=cartons)
           sev.save()
           return HttpResponseRedirect('/')
         
   else:
       ordfom=ordesform()       
       party=Clients.objects.all()


   return render(request,'addorder.html', {'orderform':ordfom,'partys':party})

def addsent(request, ordid):
   
    sento = Orders.objects.filter(id=ordid)
    sentform=Sentorderform(request.POST)
    
    ordercarton=0
    
    for c in sento :
        Ordersid=c.id
        sent_cancel=c.sent_cancel
        ordercarton=c.ordered_cartons     
       
    if request.method =='POST':
       
       if sentform.is_valid():
           date=sentform.cleaned_data['date']          
           cartons=sentform.cleaned_data['cartons']
           status=sentform.cleaned_data['status']
           by=sentform.cleaned_data['by']
           sev=Sentorder(orders_id=ordid,date=date,
           cartons=cartons,status=status,by=by)
           sentcancel=sent_cancel+cartons
           if ordercarton>=sentcancel :
             sev.save()
             Orders.objects.filter(pk=Ordersid).update(sent_cancel=sent_cancel+int(cartons),
             balance=ordercarton-sentcancel)
             return HttpResponseRedirect('/')
           else:
               
               print("corderd compliet Or Want to extra order")
           #updateorder=Orders(consignees_id=consigneeid, sent_cancel=sent_cancel+int(cartons))
           #updateorder.save()
           #sev.save()
           #return HttpResponseRedirect('/')
           sentform=Sentorderform()
    else:  
      
        sentform=Sentorderform()

    return render(request,'addsent.html',{'sentform':sentform,})   

def sent_data(request):    
    order_id = request.GET.get('orderid')        
    sentdetails = Sentorder.objects.filter(orders_id=order_id)               
    return render(request, 'sent_data.html', {'sent_details' : sentdetails,})


