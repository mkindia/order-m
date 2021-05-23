from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Clients, Consignees, Orders, Sentorder, Items
from .form import consigneeform, ordesform, Sentorderform, Clientform, Userauthform, Itemsform
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
    
      party=Clients.objects.all()   
      return render(request, "index.html", {'partys':party,'username':request.user,})
    else:
     return HttpResponseRedirect('/userlogin/')

def con_id(request):
    
    id = request.GET.get('cons1')
    cons1 = Consignees.objects.filter(party_id=id)
    return render(request, 'con_data.html', {'consi' : cons1,}) 
  

def add_consignee(request):    
    if request.method == 'POST':       
        confom=consigneeform(request.POST)  
        partyid=request.POST.get('party_id')
        consignee1=request.POST.get('consignee')
        conflict=Consignees.objects.filter(party_id=partyid)
        for i in conflict:            
            if i.consignee == consignee1:
                messages.warning(request,'Consignee Already Exist')
                return HttpResponseRedirect('/addparty/')
                 
        if confom.is_valid():
                sht=confom.cleaned_data['consignee']
                sta=confom.cleaned_data['station']           
                tr=confom.cleaned_data['trasport']
                sev=Consignees(party_id=request.POST.get('party_id'), consignee=sht, station=sta, trasport=tr)
                #sev.save()
                
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
                #pi=Consignees.objects.get(pk=Consignee_id)
                #pid= int(pi.party_id)
                sht=confom.cleaned_data['consignee']
                sta=confom.cleaned_data['station']           
                tr=confom.cleaned_data['trasport']
                #sev=Consignees(id=Consignee_id,party_id=pid, consignee=sht, station=sta, trasport=tr)
                #sev.save()   
                                 
                return HttpResponseRedirect('/')
    else:
        #con=Consignees.objects.get(pk=Consignee_id)          
        #conform=consigneeform(instance=con)        
        conform=consigneeform()
    return render(request,'editconsignee.html', {'editform':conform})

   
def order_data(request):
    
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

def add_items(request):
      if request.method=='POST':
          item=''
          itemname=request.POST.get('item_name')              
          for item1 in Items.objects.filter(item_name=itemname) :
              item=item1
            
          if str(itemname) == str(item) :
              messages.warning(request,'Item already Exist')              
              return HttpResponseRedirect('/add_items/')
          else:
              itemForms=Itemsform(request.POST)
              if itemForms.is_valid():
                  itemForms.save()          
                  return HttpResponseRedirect('/')
      else:
          itemform=Itemsform()

      return render(request,'add_items.html',{'itemforms':itemform})

def edit_items(request):
    return render(request,'edititems.html')

def item_data(request):
    item = Items.objects.all()
    
    return render(request, 'item_data.html', {'items':item})

def add_party(request):
    if request.method=='POST':
        party=''       
        n=Clients.objects.filter(party=request.POST.get('party'))
        for c in n :
            party=c.party

        if str(party)== str(request.POST.get('party')):
            messages.warning(request,'Party Already Exist')
            return HttpResponseRedirect('/addparty/')
        else:
            clients=Clientform(request.POST)
            if clients.is_valid():
               name=clients.cleaned_data['party']
               station=clients.cleaned_data['station']
               transport=clients.cleaned_data['transport']
               partsev=Clients(party=name,station=station,transport=transport)
               partsev.save()
               pid=''
               i=Clients.objects.filter(party=name)
               for id in i:
                pid=id.id
               consev=Consignees(party_id=int(pid),consignee=name,station=station,transport=transport)
               consev.save()
               return HttpResponseRedirect('/')
    else:
        clients=Clientform()
    return render(request,'addparty.html',{'clients':clients})