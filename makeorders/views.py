from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Clients, Consignees, Orders, Sentorder, Items
from .form import consigneeform, ordesform, Sentorderform, Clientform, Userauthform, Itemsform

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
   if request.user.is_authenticated:

            if request.method == 'POST':       
                confom=consigneeform(request.POST)  
                partyid=request.POST.get('party_id').title()
                consignee1=request.POST.get('consignee').title()
                conflict=Consignees.objects.filter(party_id=partyid)
                con=''
                for i in conflict:
                    con=i.consignee
                    if con == consignee1:
                        messages.warning(request,'Consignee Already Exist')
                        return HttpResponseRedirect('/addparty/')
                        
                if confom.is_valid():
                        sht=confom.cleaned_data['consignee'].title()
                        sta=confom.cleaned_data['station'].title()           
                        tr=confom.cleaned_data['transport'].title()
                        sev=Consignees(party_id=int(request.POST.get('party_id')), consignee=sht, station=sta, transport=tr)
                        sev.save()                        
                        return HttpResponseRedirect('/')
            
            else:
             party=Clients.objects.all()       
             confom=consigneeform()
   else:
      return HttpResponseRedirect('/')

            #print(id) 
   return render(request, 'add_consignee.html', {'form':confom,'partys':party})  

def edit_consignee(request, atri):
    if request.user.is_authenticated:
        client=Clients.objects.all()
    
        if atri=='edit':
            if request.method == 'POST':           
                confom=consigneeform(request.POST)
                if confom.is_valid():                
                    partyid=request.POST.get('party_id').title()
                    consignee1=request.POST.get('consignee').title()
                    pi=Consignees.objects.get(pk=request.POST.get('consigneeid').title())
                    pi.consignee      
                    conflict=Consignees.objects.filter(party_id=partyid)
                    con=''
                    noofcon=0
                    for i in conflict:
                        con=i.consignee                    
                        if con == consignee1 and consignee1 != pi.consignee :
                            noofcon+=1                        
                    if noofcon >= 1:
                        messages.warning(request,'Consignee Already Exist  '+ consignee1)                            
                    else :        
                        print(request.POST.get('consigneeid'))
                        pi=Consignees.objects.get(pk=request.POST.get('consigneeid').title())
                        pid= int(pi.party_id)
                        sht=confom.cleaned_data['consignee'].title()
                        sta=confom.cleaned_data['station'].title()          
                        tr=confom.cleaned_data['transport'].title()
                        sev=Consignees(id=request.POST.get('consigneeid'),party_id=pid, consignee=sht, station=sta, transport=tr)
                        sev.save()                
                        messages.success(request,'Consignee Updated Success'+"  "+ consignee1)                                      
                        return HttpResponseRedirect('/editconsignee/edit/')
        if atri=='delete':        
            if request.method=='POST':
                if request.POST.get('consigneeid'):
                    pid=Consignees.objects.get(pk=request.POST.get('consigneeid').title())
                    pid.delete()
                    return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
     
    return render(request,'editconsignee.html', {'partys':client})
   
def order_data(request):
    
    if request.GET.get('conid'):       
        Consignee_id=request.GET.get('conid')          
        orders = Orders.objects.filter(consignees_id=Consignee_id)     
    return render(request, 'for_data.html', {'order' : orders,})

def add_order(request, atri, oid):
     if request.user.is_authenticated:
        party=Clients.objects.all()
        items = Items.objects.all()
        item='None'   
        if atri == 'edit':         
            ordfom=Orders.objects.all()
            adfom=Orders.objects.get(pk=int(oid))
            
            ordfom=ordesform(instance=adfom)
            ordfom1=Orders.objects.filter(pk=int(oid))
            for it in ordfom1 :
                item=it.item_name
                con_id=it.consignees_id
                #print(it.item_name)
            if request.method =='POST':
                ordfom=ordesform(request.POST)
                if ordfom.is_valid():
                    date=ordfom.cleaned_data['orderdate']
                    item_name=request.POST.get('item_name')
                    item_price=ordfom.cleaned_data['item_price']
                    cartons=ordfom.cleaned_data['qty']
                    unit=ordfom.cleaned_data['unit']     
                    sev=Orders(id=oid,consignees_id=con_id,orderdate=date,
                    item_name=item_name,item_price=item_price,qty=cartons,unit=unit,balance=cartons)
                    sev.save()
                    messages.success(request,'Order update successed')
                    return HttpResponseRedirect('/')
            
        if atri == 'add':        
            if request.method =='POST':
                ordfom=ordesform(request.POST)
                if ordfom.is_valid():
                    date=ordfom.cleaned_data['orderdate']
                    item_name=request.POST.get('item_name')
                    item_price=ordfom.cleaned_data['item_price']
                    cartons=ordfom.cleaned_data['qty']
                    unit=ordfom.cleaned_data['unit']     
                    sev=Orders(consignees_id=request.POST.get('consignee_id'),orderdate=date,
                    item_name=item_name,item_price=item_price,qty=cartons,unit=unit,balance=cartons)
                    sev.save()
                    #print(ordfom.cleaned_data['item_name'])
                    messages.success(request,'Order added successed')
                    return HttpResponseRedirect('/addorder/add/0/')
                    
            else:
                ordfom=ordesform()       
     else:
         return HttpResponseRedirect('/')       
     return render(request,'addorder.html', {'orderform':ordfom,'partys':party,'sitem':item,'items':items})

def addsent(request, ordid):
    if request.user.is_authenticated:
        
            sento = Orders.objects.filter(id=ordid)
            sentform=Sentorderform(request.POST)            
            ordercarton=0            
            for c in sento :
                Ordersid=c.id
                sent_cancel=c.sent_cancel
                ordercarton=c.qty     
            
            if request.method =='POST':            
                if sentform.is_valid():
                    date=sentform.cleaned_data['date']          
                    cartons=sentform.cleaned_data['qty']
                    status=sentform.cleaned_data['status']
                    by=sentform.cleaned_data['by']
                    sev=Sentorder(orders_id=int(ordid),date=date,
                    qty=cartons,status=status,by=by)
                    sentcancel=sent_cancel+cartons
                    if ordercarton>=sentcancel :
                        sev.save()
                        Orders.objects.filter(pk=Ordersid).update(sent_cancel=sent_cancel+float(cartons),
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
    else:
        return HttpResponseRedirect('/')
    return render(request,'addsent.html',{'sentform':sentform,})   

def sent_data(request):  
    if request.user.is_authenticated:  
        order_id = request.GET.get('orderid')        
        sentdetails = Sentorder.objects.filter(orders_id=order_id)               
    else:
        return HttpResponseRedirect('/')
    return render(request, 'sent_data.html', {'sent_details' : sentdetails,})

def items(request, atri):
    if request.user.is_authenticated:
        item=Items.objects.all()
        if atri=='add':
            action='add'                  
            if request.method=='POST':
                item=''
                itemname=request.POST.get('item_name')              
                for item1 in Items.objects.filter(item_name=itemname) :
                    item=item1
                    
                if str(itemname) == str(item) :
                    messages.warning(request,'Item already Exist')              
                    return HttpResponseRedirect('/items/add/')
                else:
                    itemForms=Itemsform(request.POST)
                    if itemForms.is_valid():
                        item_name=itemForms.cleaned_data['item_name'].title()
                        sev=Items(item_name=item_name)
                        sev.save()        
                        return HttpResponseRedirect('/items/add/')
           
        if atri=='edit':
            action='edit'
            if request.POST.get('item_id'):
                pid=request.POST.get('item_id')
                itemform=Itemsform(request.POST)
                if itemform.is_valid():
                    name=itemform.cleaned_data['item_name'].title()
                    pi=Items.objects.get(pk=int(pid))
                    conflict=Items.objects.all()
                    con=''
                    noofcon=0
                    for i in conflict:
                        con=i.item_name                                     
                        if con == name and name != pi.item_name :
                            noofcon+=1                        
                    if noofcon >= 1:                        
                        messages.warning(request,'Item Already Exist  '+ name)
                        return HttpResponseRedirect('/items/edit/')                   
                    else :
                        sev=Items(id=int(pid),item_name=name)
                        sev.save()
                        messages.success(request,'Item Update Success  '+ name)
                        return HttpResponseRedirect('/items/edit/')
                                   
        if atri=='delete':
             action='delete'
             if request.method=='POST':
                if request.POST.get('item_id'):
                    pid=Items.objects.get(pk=request.POST.get('item_id').title())
                    pid.delete()
                    return HttpResponseRedirect('/')
            
    else:
        return HttpResponseRedirect('/')
    return render(request,'items.html',{'action':action,'items':item})

def add_party(request):
    if request.user.is_authenticated:  
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
                        name=clients.cleaned_data['party'].title()
                        station=clients.cleaned_data['station'].title()
                        transport=clients.cleaned_data['transport'].title()
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
    else:
        return HttpResponseRedirect('/')            
    return render(request,'addparty.html',{'clients':clients})

def edit_party(request, atri):
    if request.user.is_authenticated:
        party=Clients.objects.all()
        if atri=='edit':
            if request.method=='POST':
                    if request.POST.get('party_id'):
                        pid=request.POST.get('party_id')
                        clients=Clientform(request.POST)
                        if clients.is_valid():
                            name=clients.cleaned_data['party'].title()
                            station=clients.cleaned_data['station'].title()
                            transport=clients.cleaned_data['transport'].title()
                            pi=Clients.objects.get(pk=int(pid))
                            conflict=Clients.objects.all()
                            con=''
                            noofcon=0
                            for i in conflict:
                                con=i.party                                       
                                if con == name and name != pi.party :
                                    noofcon+=1                        
                            if noofcon >= 1:                        
                                messages.warning(request,'Party Already Exist  '+ name)
                                return HttpResponseRedirect('/editparty/edit/')                   
                            else :                        
                                partsev=Clients(id=int(pid),party=name,station=station,transport=transport)
                                partsev.save()
                                cid=''
                                i=Consignees.objects.filter(party_id=int(pid))
                                for id in i:
                                    cid=id.id
                                consev=Consignees(id=int(cid),party_id=int(pid),consignee=name,station=station,transport=transport)
                                consev.save()
                                messages.success(request,'Party Update Success  '+ name)
                                return HttpResponseRedirect('/editparty/edit/')
        if atri=='delete':
                if request.method=='POST':
                    if request.POST.get('party_id'):
                        pid=Clients.objects.get(pk=request.POST.get('party_id'))
                        pid.delete()
                        return HttpResponseRedirect('/')         
    else:
        return HttpResponseRedirect('/')

    return render(request,'editparty.html', {'partys':party})

def form_data(request, atri):
     if atri == 'party_editform':
        pk=Clients.objects.get(pk=int(request.GET.get('partyid')))
        dataform=Clientform(instance=pk)
     if atri == 'party_deleteform':
         pk=Clients.objects.get(pk=int(request.GET.get('partyid')))
         dataform=Clientform(instance=pk) 
     if atri == 'consignee_editform':
         if request.GET.get('conid') :
          pk= Consignees.objects.get(pk=int(request.GET.get('conid')))         
          dataform=consigneeform(instance=pk)
         else:
             dataform=consigneeform()
     if atri == 'consignee_deleteform':
         if request.GET.get('conid') :
          pk= Consignees.objects.get(pk=int(request.GET.get('conid')))         
          dataform=consigneeform(instance=pk)
         else:
             dataform=consigneeform()
     if atri == 'item_editform' :
         if request.GET.get('item_id'):
             pk=Items.objects.get(pk=int(request.GET.get('item_id')))
             dataform=Itemsform(instance=pk)
         else:
             dataform=Itemsform()
     if atri == 'item_deleteform' :
         if request.GET.get('item_id'):
             pk=Items.objects.get(pk=int(request.GET.get('item_id')))
             dataform=Itemsform(instance=pk)
         else:
             dataform=Itemsform()        
     if atri == 'item_addform':        
           dataform=Itemsform()      
     
     return render(request, 'form_data.html',{'form':dataform,'atri':atri})