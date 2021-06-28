
from datetime import datetime
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.http import JsonResponse
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
                    request.session['accesskey'] = 'accesskey'
                    #messages.success(request,'Success')
                    return HttpResponseRedirect('/')

        else:        
            fm=Userauthform()
        return render(request,'userlogin.html',{'form':fm})
    else:
        request.session.flush()
        request.session.clear_expired()
        return HttpResponseRedirect('/')    

#Logout user
def user_logout(request):  
    logout(request)
    request.session.flush()
    request.session.clear_expired()
    return HttpResponseRedirect('/userlogin/')   

# Create your views here.
def home(request):
    if request.user.is_authenticated:
      request.session.modified=True
      party=Clients.objects.all()   
      return render(request, "index.html", {'partys':party,'username':request.user,})
    else:
     return HttpResponseRedirect('/userlogin/')

def con_id(request):
    request.session.modified=True
    id = request.GET.get('cons1')
    cons1 = Consignees.objects.filter(party_id=id)
    return render(request, 'con_data.html', {'consi' : cons1,}) 

def add_consignee(request,pr):
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
                        if pr == 'order':              
                            return HttpResponseRedirect('/addorder/add/')
                        else:
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
   
def for_data(request):
    request.session.modified=True
    items=Items.objects.all()
    if request.GET.get('pid'):
        pid=request.GET.get('pid')
        orders = Orders.objects.filter(party_id=pid).order_by('orderdate')
        partyq=Clients.objects.get(pk=pid)
        party=partyq.party
        conq=Consignees.objects.filter(party_id=pid)
               

    if request.GET.get('conid'):
        conid=request.GET.get('conid')
        orders = Orders.objects.filter(consignees_id=conid).order_by('orderdate')
        partyq=Consignees.objects.get(pk=conid)
        party=partyq.party
        conq=Consignees.objects.filter(pk=conid)
    return render(request, 'for_data.html', {'order' : orders,'item':items,'party':party,'con':conq})

def add_order(request, atri):
     if request.user.is_authenticated:
        party=Clients.objects.all()
        items = Items.objects.all()
        item='None'   
        if atri == 'edit':
                oid=request.GET.get('oid', None)                             
                ordfom=Orders.objects.all()
                adfom=Orders.objects.get(pk=int(oid))                
                ordfom=ordesform(instance=adfom)
                ordfom1=Orders.objects.filter(pk=int(oid))
                for it in ordfom1 :
                    item=it.item_id
                    con_id=it.consignees_id
                    party_id=it.party_id
                    #print(it.item_name)
                if request.method =='POST':
                    ordfom=ordesform(request.POST)
                    if ordfom.is_valid():
                        date=ordfom.cleaned_data['orderdate']
                        item_id=request.POST.get('item_id')
                        item_price=ordfom.cleaned_data['item_price']
                        cartons=ordfom.cleaned_data['qty']
                        unit=ordfom.cleaned_data['unit']     
                        sev=Orders(id=oid,consignees_id=con_id,party_id=party_id,orderdate=date,
                        item_id=item_id,item_price=item_price,qty=cartons,unit=unit,balance=cartons)
                        sev.save()
                        messages.success(request,'Order update successed')
                        return HttpResponseRedirect('/')        
        if atri == 'add':        
            if request.method =='POST':
                ordfom=ordesform(request.POST)
                if ordfom.is_valid():
                    date=ordfom.cleaned_data['orderdate']
                    item_id=request.POST.get('item_id')
                    item_price=ordfom.cleaned_data['item_price']
                    cartons=ordfom.cleaned_data['qty']
                    unit=ordfom.cleaned_data['unit']     
                    sev=Orders(consignees_id=request.POST.get('consignee_id'),party_id=request.POST.get('party_id'),orderdate=date,
                    item_id=item_id,item_price=item_price,qty=cartons,unit=unit,balance=cartons)
                    sev.save()
                    #print(ordfom.cleaned_data['item_name'])
                    messages.success(request,'Order added successed')
                    return HttpResponseRedirect('/addorder/add/')
            else:
                ordfom=ordesform()        
        if atri == 'delete':
            if request.method =='POST':                
                orderid=Orders.objects.get(pk=request.POST.get('oid'))
                orderid.delete()
                return HttpResponseRedirect('/')
     else:
         return HttpResponseRedirect('/')       
     return render(request,'addorder.html', {'orderform':ordfom,'partys':party,'sitem':item,'items':items})

def addsent(request, atri):
    if request.user.is_authenticated:
        action=atri
        con=Consignees.objects.all()
        if atri=='add':
            sento = Orders.objects.filter(id= request.GET.get('oid'))            
            sentform=Sentorderform()            
            ordercarton=0               
            findconsignee=0
            for c in sento :
                Ordersid=c.id
                sent_cancel=c.sent_cancel
                ordercarton=c.qty 
                findconsignee=c.consignees_id
            fclient=Consignees.objects.get(pk=findconsignee) # for Client Id
            trsferto=Consignees.objects.filter(party_id=fclient.party_id) # for consignee id
           
            if request.method =='POST':
                sentform=Sentorderform(request.POST)         
                if sentform.is_valid():                  
                    date=sentform.cleaned_data['date']          
                    cartons=sentform.cleaned_data['qty']
                    status=sentform.cleaned_data['status']
                    by=sentform.cleaned_data['by']
                    if request.POST.get('Con_id'):
                        findconsignee=request.POST.get('Con_id')
                    sev=Sentorder(orders_id=request.GET.get('oid'),date=date,
                    qty=cartons,status=status,consignee_id=findconsignee,by=by)
                    sentcancel=sent_cancel+cartons
                    
                    if ordercarton>=sentcancel :
                        sev.save()
                        Orders.objects.filter(pk=Ordersid).update(sent_cancel=sent_cancel+float(cartons),
                        balance=ordercarton-sentcancel)
                        if status == 'Transfer To Consignee':
                                    transferorder=Orders(consignees_id=request.POST.get('Con_id'),orderdate=date,
                                    item_id=request.GET.get('item_id'),item_price=request.GET.get('item_price'),
                                    qty=cartons,unit=request.GET.get('unit'),balance=cartons)
                                    transferorder.save()
                        return HttpResponseRedirect('/')
                    else:
                     
                        messages.warning(request,'Order Balance is Less then Sent Order please add First')
                        sentform=Sentorderform()
                      
                else:  
                
                    sentform=Sentorderform()

        if atri=='edit':
            sq=Sentorder.objects.get(pk=request.GET.get('sid'))                          
            sentform=Sentorderform(instance=sq)
            seqty=0
            oid=0
            seid=0
            sdetail=Sentorder.objects.filter(pk=request.GET.get('sid'))
            for sde in sdetail:
                seqty=sde.qty
                oid=sde.orders_id
                seid=sde.id
            sento = Orders.objects.filter(pk=oid)                   
            ordercarton=0               
            findconsignee=0
            obal=0
            for c in sento :
                Ordersid=c.id
                sent_cancel=c.sent_cancel
                ordercarton=c.qty 
                findconsignee=c.consignees_id
                obal=c.balance
            totalbal=obal+seqty         
            fclient=Consignees.objects.get(pk=findconsignee) # for Client Id
            trsferto=Consignees.objects.filter(party_id=fclient.party_id) # for consignee id 
            
            if request.method =='POST':
                sentform=Sentorderform(request.POST)
                if sentform.is_valid():                  
                    date=sentform.cleaned_data['date']          
                    cartons=sentform.cleaned_data['qty']
                    status=sentform.cleaned_data['status']
                    by=sentform.cleaned_data['by']
                    sentcancel=sent_cancel+cartons-seqty
                    if request.POST.get('Con_id'):
                        findconsignee=request.POST.get('Con_id')
                    if ordercarton>=sentcancel :
                        Sentorder.objects.filter(pk=seid).update(date=date,qty=cartons,
                        status=status,consignee_id=findconsignee,by=by)

                        Orders.objects.filter(pk=Ordersid).update(sent_cancel=sent_cancel+float(cartons)-float(seqty),
                        balance=ordercarton-sentcancel)
                       
                        messages.success(request,'Update Success')
                        return HttpResponseRedirect('/')
                    else:                     
                        messages.warning(request,'Order Balance is Less then Sent Order please add First')

        if atri=='delete':
                sdetail=Sentorder.objects.filter(pk=request.POST.get('sid'))
                for sde in sdetail:
                    seqty=sde.qty
                    oid=sde.orders_id                
                sento = Orders.objects.filter(pk=oid)               
                for c in sento :
                    Ordersid=c.id
                    sent_cancel=c.sent_cancel                
                    obal=c.balance             
                   
                Orders.objects.filter(pk=Ordersid).update(sent_cancel=sent_cancel-float(seqty),
                balance=obal+float(seqty))

                rsent=Sentorder.objects.get(pk=request.POST.get('sid'))                
                rsent.delete()

                #messages.success(request,'Update Success')
                return HttpResponseRedirect('/')
                


    else:
        return HttpResponseRedirect('/')
    return render(request,'addsent.html',{'sentform':sentform,'action':action,'con':con,'transferto':trsferto})   

def sent_data(request):
    if request.user.is_authenticated:  
        con=Consignees.objects.all()
        order_id = request.GET.get('orderid')        
        sentdetails = Sentorder.objects.filter(orders_id=order_id)               
    else:
        return HttpResponseRedirect('/')
    return render(request, 'sent_data.html', {'sent_details' : sentdetails,'consignees':con})

def items(request, atri, pr):
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
                        if pr == 'order':
                            return HttpResponseRedirect('/addorder/add/')
                        else:
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
                    item1='None'                           
                    ordfom=Orders.objects.filter(item_id=request.POST.get('item_id'))
                    for it in ordfom : 
                        item1=it.item_id               
                    
                    if item1 == 'None':                         
                        pid=Items.objects.get(pk=request.POST.get('item_id'))                 
                        pid.delete()
                    else:
                        itemname=Items.objects.filter(pk=request.POST.get('item_id'))
                        for inn in itemname:
                             item1=inn.item_name      
                            
                    response = {'msg':item1} # response message
                    return JsonResponse(response) # return response as JSON
                     
    else:
        return HttpResponseRedirect('/')
    return render(request,'items.html',{'action':action,'items':item})

def add_party(request,pr):
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
                        if pr == 'order':    
                            return HttpResponseRedirect('/addorder/add/')
                        else:
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
     if atri == 'addsent':
         if request.POST.get('oid'):
             dataform=consigneeform.objects.get('consignee')

             
     
     return render(request, 'form_data.html',{'form':dataform,'atri':atri})

def item_wise(request,filter):    
    if request.user.is_authenticated:
        if filter == 'item_wise':
            items=Items.objects.all()            
            data={'item':items,'filter':filter}
        if filter == 'date_wise':            
            items=Items.objects.all()            
            data={'item':items,'filter':filter}
    else:    
        return HttpResponseRedirect('/')

    return render(request,'itemwiseorders.html',data)

def itemwise_data(request,filter):
    if request.method=='POST':
        if filter == 'item_wise':
            item1=request.POST.get('item_id')
            items=Items.objects.filter(pk=int(item1))
            orders=Orders.objects.filter(item_id=item1).order_by('orderdate')
            con=Consignees.objects.all()
            party=Clients.objects.all()
            data={'order':orders,'item':items,'consignees':con,'partys':party,'filter':filter}
        if filter == 'date_wise':
            items=Items.objects.all()
            orders=Orders.objects.all().order_by('orderdate').order_by('orderdate')
            con=Consignees.objects.all()
            party=Clients.objects.all()
            data={'order':orders,'item':items,'consignees':con,'partys':party,'filter':filter}

    return render(request,'itemwise_data.html',data)