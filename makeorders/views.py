
from django.http import response
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotModified
from django.utils import timezone

from django.shortcuts import redirect, render, HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Clients, Consignees, Orders, Sentorder, Items
from .form import consigneeform, ordesform, Sentorderform, Clientform, Userauthform, Itemsform
from django.views.decorators.cache import cache_control
# User Login form


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = Userauthform(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                vuser = authenticate(username=uname, password=upass)
                if vuser is not None:
                    login(request, vuser)
                    request.session['accesskey'] = 'accesskey'
                    # superuser=request.user.is_superuser
                    # messages.success(request,suer)
                    return redirect('/')
                    #return HttpResponseRedirect('/')

        else:
            fm = Userauthform()
            return render(request, 'userlogin.html', {'form': fm})
    else:
        request.session.flush()
        request.session.clear_expired()
        return redirect('/')

# Logout user
def user_logout(request):
    logout(request)
    request.session.flush()
    request.session.clear_expired()
    return HttpResponseRedirect('/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    fm = Userauthform()
    if request.user.is_authenticated:
        sf=Sentorderform()
        request.session.modified = True
        party = Clients.objects.all().order_by('party')
        return render(request, "index.html", {'partys': party, 'username': request.user,'sf':sf })
    else:
        party = Clients.objects.all().order_by('party')
        if request.method == 'POST':            
            fm = Userauthform(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                vuser = authenticate(username=uname, password=upass)
                if vuser is not None:
                    login(request, vuser)
                    request.session['accesskey'] = 'accesskey'                   
                    return redirect('/')
        else:
             request.session.flush()
             request.session.clear_expired()
        return render(request, "index.html", {'partys': party, 'username': request.user, 'form':fm })

def con_id(request, atri):
    request.session.modified = True
    id = request.GET.get('cons1')
    cons1 = Consignees.objects.filter(party_id=id).order_by('consignee')
    return render(request, 'con_data.html', {'consi': cons1, 'atri': atri})


def add_consignee(request, pr):
    if request.user.is_authenticated:
       
      if pr == 'order':
          if request.is_ajax() or request.method == 'POST':
                    consignee1 = request.POST.get('id_consignee').title()
                    station = request.POST.get('id_station').title()
                    transport = request.POST.get('id_transport').title()
                    partyid = request.POST.get('id_party')                   
                    conflict = Consignees.objects.filter(party_id=partyid)
                    con = ''
                    for i in conflict: 
                         if i.consignee == consignee1:
                            con = i.consignee
                         
                    if con != consignee1:
                        sev = Consignees(party_id=partyid, consignee=consignee1, station=station, transport=transport)
                        sev.save()
                        return HttpResponse('Success')
                    else:
                        return HttpResponseBadRequest()
          
      else:
        if request.method == 'POST':

            confom = consigneeform(request.POST)
            partyid = request.POST.get('party_id').title()
            consignee1 = request.POST.get('consignee').title()
            conflict = Consignees.objects.filter(party_id=partyid)
            con = ''
            for i in conflict:
                if i.consignee == consignee1:
                            con = i.consignee                
            if con == consignee1:
                    messages.warning(request, 'Consignee Already Exist')
                    return HttpResponseRedirect('/addconsignee/addcon/')
            else :
                if confom.is_valid():
                    sht = confom.cleaned_data['consignee'].title()
                    sta = confom.cleaned_data['station'].title()
                    tr = confom.cleaned_data['transport'].title()
                    sev = Consignees(party_id=int(request.POST.get(
                        'party_id')), consignee=sht, station=sta, transport=tr)
                    sev.save()
                    messages.success(request,'Consignee Added Success')
                    return redirect('/addconsignee/addcon/')

        else:
            party = Clients.objects.all()
            confom = consigneeform()
            return render(request, 'add_consignee.html', {'form': confom, 'partys': party})

    else:
        return HttpResponseRedirect('/')

        # print(id)
    

def edit_consignee(request, atri):
    if request.user.is_authenticated:
        client = Clients.objects.all()

        if atri == 'edit':
            if request.method == 'POST':
                confom = consigneeform(request.POST)
                if confom.is_valid():
                    partyid = request.POST.get('party_id').title()
                    consignee1 = request.POST.get('consignee').title()
                    pi = Consignees.objects.get(
                        pk=request.POST.get('consigneeid').title())
                    pi.consignee
                    conflict = Consignees.objects.filter(party_id=partyid)
                    con = ''
                    noofcon = 0
                    for i in conflict:
                        con = i.consignee
                        if con == consignee1 and consignee1 != pi.consignee:
                            noofcon += 1
                    if noofcon >= 1:
                        messages.warning(
                            request, 'Consignee Already Exist  ' + consignee1)
                    else:
                        pi = Consignees.objects.get(
                            pk=request.POST.get('consigneeid').title())
                        pid = int(pi.party_id)
                        sht = confom.cleaned_data['consignee'].title()
                        sta = confom.cleaned_data['station'].title()
                        tr = confom.cleaned_data['transport'].title()
                        Consignees.objects.filter(id=request.POST.get('consigneeid')).update(
                            party_id=pid, consignee=sht, station=sta, transport=tr)

                        messages.success(
                            request, 'Consignee Updated Success'+"  " + consignee1)
                        return HttpResponseRedirect('/editconsignee/edit/')
        if atri == 'delete':
            if request.method == 'POST':
                if request.POST.get('consigneeid'):
                    pid = Consignees.objects.get(pk=request.POST.get('consigneeid').title())
                    if pid.party_consignee == None:                       
                        pid.delete()
                        messages.warning(request, 'Consignee Delete Success')
                        return HttpResponseRedirect('/')
                    else:
                        messages.success(request,'Consignee not Delete it Primary')
                        return redirect('/editconsignee/delete/')
    else:
        return HttpResponseRedirect('/')

    return render(request, 'editconsignee.html', {'partys': client})


def consigneeDetails(request):
    allconsignee = Consignees.objects.all()
    return render(request, "consigneedetails.html", {'allcon': allconsignee})


def for_data(request, atri):
    request.session.modified = True
    items = Items.objects.all()
    if request.GET.get('pid'):
        pid = request.GET.get('pid')
        orders = Orders.objects.filter(party_id=pid).order_by('orderdate')
        partyq = Clients.objects.get(pk=pid)
        party = partyq.party
        conq = Consignees.objects.filter(party_id=pid)

    if request.GET.get('conid'):
        conid = request.GET.get('conid')
        orders = Orders.objects.filter(
            consignees_id=conid).order_by('orderdate')
        partyq = Consignees.objects.get(pk=conid)
        party = partyq.party
        conq = Consignees.objects.filter(pk=conid)
    return render(request, 'for_data.html', {'order': orders, 'item': items, 'party': party, 'con': conq, 'atri':atri})


def add_order(request, atri):
    if request.user.is_authenticated:
        ordfom = ordesform()
        party = Clients.objects.all().order_by('party')
        items = Items.objects.all().order_by('item_name')
        item = 'None'
        if atri == 'edit':
            oid = request.GET.get('oid', None)
            ordfom = Orders.objects.all()
            adfom = Orders.objects.get(pk=int(oid))
            ordfom = ordesform(instance=adfom)
            ordfom1 = Orders.objects.filter(pk=int(oid))
            for it in ordfom1:
                item = it.item_id
                con_id = it.consignees_id
                party_id = it.party_id
                # print(it.item_name)
            if request.method == 'POST':
                ordfom = ordesform(request.POST)
                if ordfom.is_valid():
                    date = ordfom.cleaned_data['orderdate']
                    item_id = request.POST.get('item_id')
                    item_des = request.POST.get('item_des')
                    item_price = ordfom.cleaned_data['item_price']
                    per = ordfom.cleaned_data['per']
                    cartons = ordfom.cleaned_data['qty']
                    unit = ordfom.cleaned_data['unit']
                    comment = ordfom.cleaned_data['comment']
                    oupdate = Orders.objects.get(pk=oid)
                    oupdate.orderdate = date
                    oupdate.item_id = item_id
                    oupdate.item_des = item_des
                    oupdate.balance = cartons
                    oupdate.item_price = item_price
                    oupdate.per = per
                    oupdate.qty = cartons
                    oupdate.unit = unit
                    oupdate.updated_at = timezone.now()
                    oupdate.comment = comment
                    oupdate.save()
                    messages.success(request, 'Order update successed')
                    return HttpResponseRedirect('/')
        if atri == 'add':
            if request.method == 'POST':
                data = request.POST.getlist('info[]')
                # where 9 is 9 record in data 0 to 8
                datarow = int(len(data)/10)
                for i in range(datarow):
                    k = (i+1)
                    j = i*10
                    d = []
                    for t in range(j, k*10):
                        d.append(data[t])

                    party_id = d[0]
                    conid = d[1]
                    date = d[2]
                    item_id = d[3]
                    item_des = d[4]
                    cartons = d[5]
                    unit = d[6]
                    item_price = d[7]
                    comment = d[8]
                    per = d[9]
                    sev = Orders(consignees_id=conid, party_id=party_id, orderdate=date, per=per,
                                 item_id=item_id, item_des=item_des, item_price=item_price, qty=cartons, unit=unit, balance=cartons, comment=comment)
                    sev.save()

                return HttpResponseRedirect('/addorder/add/')

            else:
                ordfom = ordesform()

        if atri == 'delete':
            if request.method == 'POST':
                orderid = Orders.objects.get(pk=request.POST.get('oid'))
                orderid.delete()

    else:
        return HttpResponseRedirect('/')
    return render(request, 'addorder.html', {'orderform': ordfom, 'partys': party, 'sitem': item, 'items': items, 'atri': atri})


def addsent(request, atri):
    if request.user.is_authenticated:
        action = atri
        con = Consignees.objects.all()
        if atri == 'add':
            if request.method == 'POST':
                oid = request.POST.get('oid')
                print(oid)                
                sento = Orders.objects.filter(id=oid)
                for c in sento:
                    Ordersid = c.id
                    sent_cancel = c.sent_cancel
                    ordercarton = c.qty
                    findconsignee = c.consignees_id
                fclient = Consignees.objects.get(pk=findconsignee)  # for Client Id
                trsferto = Consignees.objects.filter(party_id=fclient.party_id)  # for consignee id
                
                date = request.POST.get('date')
                item_id = request.POST.get('item_id')
                cartons =  request.POST.get('qty')
                unit = request.POST.get('unit')
                status = request.POST.get('status')
                price = request.POST.get('price')
                by = request.POST.get('by')
                bal = request.POST.get('bal')
                transid = request.POST.get('transid')
                
                sev = Sentorder(orders_id=oid, date=date,
                                    qty=cartons, status=status, consignee_id=findconsignee, by=by, updated_at=timezone.now)
                sev.save()
                Orders.objects.filter(pk=Ordersid).update(sent_cancel=sent_cancel+float(cartons),
                                                                  balance=bal)

                if status == 'Transfer':
                            latestsent = Sentorder.objects.latest('updated_at')
                            transferorder = Orders(party_id=fclient.party_id, consignees_id=transid, orderdate=date,
                                                   item_id=item_id, item_price=price,
                                                   qty=cartons, unit=unit, balance=cartons, sent_trs_id=latestsent.id)
                            transferorder.save()
                            soi = Orders.objects.get(sent_trs_id=latestsent.id)
                            Sentorder.objects.filter(pk=latestsent.id).update(order_trs_id=soi.id,consignee_id=transid)
                return redirect('/')
                """
                sev.save()
                Orders.objects.filter(pk=Ordersid).update(sent_cancel=sent_cancel+float(cartons),
                                                                  balance=ordercarton-sentcancel)
                if status == 'Transfer To':
                            latestsent = Sentorder.objects.latest('updated_at')
                            transferorder = Orders(party_id=fclient.party_id, consignees_id=request.POST.get('Con_id'), orderdate=date,
                                                   item_id=request.GET.get('item_id'), item_price=request.GET.get('item_price'),
                                                   qty=cartons, unit=request.GET.get('unit'), balance=cartons, sent_trs_id=latestsent.id)
                            transferorder.save()
                            soi = Orders.objects.get(sent_trs_id=latestsent.id)
                            Sentorder.objects.filter(
                                pk=latestsent.id).update(order_trs_id=soi.id) """


            
        """
            sento = Orders.objects.filter(id=request.GET.get('oid'))
            sentform = Sentorderform()
            bal = request.GET.get('bal')
            ordercarton = 0
            findconsignee = 0
            for c in sento:
                Ordersid = c.id
                sent_cancel = c.sent_cancel
                ordercarton = c.qty
                findconsignee = c.consignees_id
            fclient = Consignees.objects.get(pk=findconsignee)  # for Client Id
            trsferto = Consignees.objects.filter(
                party_id=fclient.party_id)  # for consignee id

            if request.method == 'POST':
                sentform = Sentorderform(request.POST)
                if sentform.is_valid():
                    date = sentform.cleaned_data['date']
                    cartons = sentform.cleaned_data['qty']
                    status = sentform.cleaned_data['status']
                    by = sentform.cleaned_data['by']
                    if request.POST.get('Con_id'):
                        findconsignee = request.POST.get('Con_id')
                    sev = Sentorder(orders_id=request.GET.get('oid'), date=date,
                                    qty=cartons, status=status, consignee_id=findconsignee, by=by, updated_at=timezone.now)
                    sentcancel = sent_cancel+cartons

                    if ordercarton >= sentcancel:
                        sev.save()
                        Orders.objects.filter(pk=Ordersid).update(sent_cancel=sent_cancel+float(cartons),
                                                                  balance=ordercarton-sentcancel)
                        if status == 'Transfer To':
                            latestsent = Sentorder.objects.latest('updated_at')
                            transferorder = Orders(party_id=fclient.party_id, consignees_id=request.POST.get('Con_id'), orderdate=date,
                                                   item_id=request.GET.get('item_id'), item_price=request.GET.get('item_price'),
                                                   qty=cartons, unit=request.GET.get('unit'), balance=cartons, sent_trs_id=latestsent.id)
                            transferorder.save()
                            soi = Orders.objects.get(sent_trs_id=latestsent.id)
                            Sentorder.objects.filter(
                                pk=latestsent.id).update(order_trs_id=soi.id)

                        messages.success(request, 'Order sent Success')
                        return redirect('/')
                    else:

                        messages.warning(
                            request, 'Order Balance is Less then Sent Order please add First')
                        sentform = Sentorderform()

                else:

                    sentform = Sentorderform()
            else:
                return render(request, 'addsent.html', {'sentform': sentform, 'bal': bal, 'action': action, 'transferto': trsferto}) """
        if atri == 'edit':
            sid = request.GET.get('sid')
            sdetail = Sentorder.objects.get(pk=sid)
            sentform = Sentorderform(instance=sdetail)

            seqty = sdetail.qty
            oid = sdetail.orders_id
            seid = sdetail.id
            order_trs_id = sdetail.order_trs_id

            sento = Orders.objects.get(pk=oid)

            Ordersid = sento.id
            item_id = sento.item_id
            item_price = sento.item_price
            sent_cancel = sento.sent_cancel
            ordercarton = sento.qty
            unit = sento.unit
            findconsignee = sento.consignees_id
            obal = sento.balance

            if order_trs_id != None:
                trto = Orders.objects.get(pk=order_trs_id)
                trsent_cancel = trto.sent_cancel

            fclient = Consignees.objects.get(pk=findconsignee)  # for Client Id
            trsferto = Consignees.objects.filter(
                party_id=fclient.party_id)  # for consignee id
            # for update transfer consignee order

            if request.method == 'POST':
                sentform = Sentorderform(request.POST)
                if sentform.is_valid():
                    date = sentform.cleaned_data['date']
                    cartons = sentform.cleaned_data['qty']
                    status = sentform.cleaned_data['status']
                    by = sentform.cleaned_data['by']
                    sentcancel = sent_cancel+cartons-seqty
                    if request.POST.get('Con_id'):
                        findconsignee = request.POST.get('Con_id')
                    if ordercarton >= sentcancel:

                        if order_trs_id != None and status != 'Transfer':     # if orderder transfer to consignee

                            # order data update
                            oupdate = Orders.objects.get(pk=Ordersid)
                            oupdate.sent_cancel = sent_cancel + \
                                float(cartons)-float(seqty)
                            oupdate.balance = ordercarton-sentcancel
                            oupdate.save()
                            # sent data update
                            supdate = Sentorder.objects.get(pk=seid)
                            supdate.date = date
                            supdate.qty = cartons
                            supdate.status = status
                            supdate.consignee_id = findconsignee
                            supdate.by = by
                            supdate.order_trs_id = None
                            supdate.save()
                            # trsfer data delete
                            ord = Orders.objects.get(pk=order_trs_id)
                            ord.delete()
                        elif order_trs_id == None and status == 'Transfer':
                            transferorder = Orders(party_id=fclient.party_id, consignees_id=request.POST.get('Con_id'), orderdate=date,
                                                   item_id=item_id, item_price=item_price,
                                                   qty=cartons, unit=unit, balance=cartons, sent_trs_id=sid)
                            transferorder.save()

                            # find last record from data table
                            latestsent = Orders.objects.latest('created_at')
                            supdate = Sentorder.objects.get(pk=seid)
                            supdate.date = date
                            supdate.qty = cartons
                            supdate.status = status
                            supdate.consignee_id = findconsignee
                            supdate.by = by
                            supdate.order_trs_id = latestsent.id
                            supdate.save()

                            oupdate = Orders.objects.get(pk=Ordersid)
                            oupdate.sent_cancel = sent_cancel + \
                                float(cartons)-float(seqty)
                            oupdate.balance = ordercarton-sentcancel

                        elif order_trs_id != None and status == 'Transfer':  # when trsfer to consinee and data same

                            troupdate = Orders.objects.get(pk=order_trs_id)
                            troupdate.orderdate = date
                            troupdate.qty = cartons
                            troupdate.consignees_id = findconsignee
                            troupdate.balance = cartons-trsent_cancel
                            troupdate.save()

                            oupdate = Orders.objects.get(pk=Ordersid)
                            oupdate.sent_cancel = sent_cancel + \
                                float(cartons)-float(seqty)
                            oupdate.balance = ordercarton-sentcancel
                            oupdate.save()

                            supdate = Sentorder.objects.get(pk=seid)
                            supdate.date = date
                            supdate.qty = cartons
                            supdate.status = status
                            supdate.consignee_id = findconsignee
                            supdate.by = by
                            supdate.save()

                        else:   # update data when not trafer order find
                            oupdate = Orders.objects.get(pk=Ordersid)
                            oupdate.sent_cancel = sent_cancel + \
                                float(cartons)-float(seqty)
                            oupdate.balance = ordercarton-sentcancel
                            oupdate.save()

                            supdate = Sentorder.objects.get(pk=seid)
                            supdate.date = date
                            supdate.qty = cartons
                            supdate.status = status
                            supdate.consignee_id = findconsignee
                            supdate.by = by
                            supdate.save()

                        messages.success(request, 'Update Success')
                        return HttpResponseRedirect('/')
                    else:
                        messages.warning(
                            request, 'Order Balance is Less then Sent Order please add First')
            else:
                return render(request, 'addsent.html', {'sentform': sentform, 'action': action, 'con': con, 'transferto': trsferto})


        if atri == 'delete':
            if request.method == 'POST':
                sid = request.POST.get('sid')
                sdetail = Sentorder.objects.get(pk=sid)
                seqty = sdetail.qty
                oid = sdetail.orders_id
                status = sdetail.status
                order_trs_id = sdetail.order_trs_id

                sento = Orders.objects.get(pk=oid)
                Ordersid = sento.id
                sent_cancel = sento.sent_cancel
                obal = sento.balance
                sent_trs_id = sento.sent_trs_id

                # oupdate=Orders.objects.get(pk=Ordersid)
                sento.sent_cancel = sent_cancel-float(seqty)
                sento.balance = obal+float(seqty)
                sento.save()
                if order_trs_id != None:
                    rco = Orders.objects.get(pk=order_trs_id)
                    rco.delete()
                rsent = Sentorder.objects.get(pk=sid)
                rsent.delete()

                return HttpResponseRedirect('/')

    else:
        
        return HttpResponseRedirect('/')
        

def sent_data(request):
    if request.user.is_authenticated:
        con = Consignees.objects.all()
        order_id = request.GET.get('orderid')
        sentdetails = Sentorder.objects.filter(orders_id=order_id)
    else:
        return HttpResponseRedirect('/')
    return render(request, 'sent_data.html', {'sent_details': sentdetails, 'consignees': con})


def items(request, atri):
    action = atri
    if request.user.is_authenticated:
        item = Items.objects.all().order_by('item_name')
        if atri == 'add':
            if request.method == 'POST':
                item = ''
                itemname = request.POST.get('item_name').title()
                for item1 in Items.objects.filter(item_name=itemname):
                    item = item1

                if str(itemname) == str(item):
                    messages.warning(request, 'Item already Exist')
                    return HttpResponseRedirect('/items/add/')
                else:
                    itemForms = Itemsform(request.POST)
                    if itemForms.is_valid():
                        item_name = itemForms.cleaned_data['item_name'].title()
                        sev = Items(item_name=item_name, item_group_id=int(1))
                        sev.save()
                        messages.success(
                            request, 'Item Save Success  ' + item_name)
                        # return HttpResponseRedirect('/items_data/')

        if atri == 'edit':

            if request.POST.get('selectedItem'):

                # pid=Items.objects.get(item_name=request.POST.get('selectedItem').title())
                pid = request.POST.get('selectedItem')
                itemform = Itemsform(request.POST)
                if itemform.is_valid():
                    name = itemform.cleaned_data['item_name'].title()
                    pi = Items.objects.get(pk=pid)
                    conflict = Items.objects.all()
                    con = ''
                    noofcon = 0
                    for i in conflict:
                        con = i.item_name
                        if con == name and name != pi.item_name:
                            noofcon += 1
                    if noofcon >= 1:
                        messages.warning(
                            request, 'Item Already Exist  ' + name)
                        return HttpResponseRedirect('/items/edit/')
                    else:
                        sev = Items.objects.get(id=pid)
                        sev.item_name = name
                        sev.save()
                        messages.success(
                            request, 'Item Update Success  ' + name)
                        return HttpResponseRedirect('/items/edit/')

        if atri == 'delete':
            print(request.POST.get('item_id'))
            if request.method == 'POST':
                item_id = request.POST.get('item_id')
                if request.POST.get('item_id'):

                    item1 = 'None'
                    ordfom = Orders.objects.filter(item_id=item_id)
                    for item in ordfom:
                        item1 = item.item_id

                    if item1 == 'None':
                        pid = Items.objects.get(pk=item_id)
                        pid.delete()
                    else:
                        itemname = Items.objects.filter(pk=item_id)
                        for inn in itemname:
                            item1 = inn.item_name

                    response = {'msg': item1}  # response message
                    return JsonResponse(response)  # return response as JSON

    else:
        return HttpResponseRedirect('/')
    return render(request, 'items.html', {'action': action, 'items': item})


def items_data(request):
    item = Items.objects.all()
    sitem = item.latest('updated_at')
    lastitemname = sitem.item_name
    lastitemid = int(sitem.id)
    response = {'sid': lastitemid, 'sitem': lastitemname, 'items': item}

    # return JsonResponse(response)
    # return response.HttpResponse(response)
    return render(request, 'items_data.html', response)


def add_party(request, pr):
    if request.user.is_authenticated:
        if request.method == 'POST':
            party = ''
            n = Clients.objects.filter(party=request.POST.get('party'))
            for c in n:
                party = c.party

            if str(party) == str(request.POST.get('party')):
                messages.warning(request, 'Party Already Exist')
                return redirect('/addparty/')
            else:
                clients = Clientform(request.POST)
                if clients.is_valid():
                    name = clients.cleaned_data['party'].title()
                    station = clients.cleaned_data['station'].title()
                    transport = clients.cleaned_data['transport'].title()
                    partsev = Clients(
                        party=name, station=station, transport=transport)
                    partsev.save()
                    pid = ''
                    i = Clients.objects.filter(party=name)
                    for id in i:
                        pid = id.id
                    consev = Consignees(party_id=int(pid), consignee=name, party_consignee=int(
                        pid), station=station, transport=transport)
                    consev.save()
                    return redirect('/')
                if pr == 'order':
                        p_name=request.POST.get('id_party').title()
                        s_name=request.POST.get('id_station').title()
                        t_name=request.POST.get('id_transport').title()
                        padd = Clients(party=p_name, station=s_name, transport=t_name)
                        padd.save()
                        pid = ''
                        i = Clients.objects.filter(party=p_name)
                        for id in i:
                          pid = id.id
                        consev = Consignees(party_id=int(pid), consignee=p_name, party_consignee=int(
                        pid), station=s_name, transport=t_name)
                        consev.save()
                        #messages.success(request, 'Party add Success  ' + name)
                        #return redirect('/addorder/add/')
                
                        

        else:
            clients = Clientform()
    else:
        return redirect('/')
    return render(request, 'addparty.html', {'clients': clients})


def edit_party(request, atri):
    if request.user.is_authenticated:
        party = Clients.objects.all()
        if atri == 'edit':
            if request.method == 'POST':
                if request.POST.get('party_id'):
                    pid = request.POST.get('party_id')
                    clients = Clientform(request.POST)
                    if clients.is_valid():
                        name = clients.cleaned_data['party'].title()
                        station = clients.cleaned_data['station'].title()
                        transport = clients.cleaned_data['transport'].title()
                        pi = Clients.objects.get(pk=int(pid))
                        conflict = Clients.objects.all()
                        con = ''
                        noofcon = 0
                        for i in conflict:
                            con = i.party
                            if con == name and name != pi.party:
                                noofcon += 1
                        if noofcon >= 1:
                            messages.warning(
                                request, 'Party Already Exist  ' + name)
                            return HttpResponseRedirect('/editparty/edit/')
                        else:
                            Clients.objects.filter(id=int(pid)).update(
                                party=name, station=station, transport=transport)

                            cid = ''
                            i = Consignees.objects.filter(party_id=int(pid))
                            for id in i:
                                cid = id.id
                            Consignees.objects.filter(id=int(cid)).update(party_id=int(
                                pid), consignee=name, station=station, transport=transport)

                            messages.success(
                                request, 'Party Update Success  ' + name)
                            return HttpResponseRedirect('/editparty/edit/')
        if atri == 'delete':
            if request.method == 'POST':
                if request.POST.get('party_id'):
                    pid = Clients.objects.get(pk=request.POST.get('party_id'))
                    pid.delete()
                    return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

    return render(request, 'editparty.html', {'partys': party})


def form_data(request, atri):

    if atri == 'party_editform':
        pk = Clients.objects.get(pk=int(request.GET.get('partyid')))
        dataform = Clientform(instance=pk)
    if atri == 'party_deleteform':
        pk = Clients.objects.get(pk=int(request.GET.get('partyid')))
        dataform = Clientform(instance=pk)
    if atri == 'consignee_editform':
        if request.GET.get('conid'):
            pk = Consignees.objects.get(pk=int(request.GET.get('conid')))
            dataform = consigneeform(instance=pk)
        else:
            dataform = consigneeform()
    if atri == 'consignee_deleteform':
        if request.GET.get('conid'):
            pk = Consignees.objects.get(pk=int(request.GET.get('conid')))
            dataform = consigneeform(instance=pk)
        else:
            dataform = consigneeform()
    if atri == 'item_editform':
        if request.GET.get('item_id'):
            pk = Items.objects.get(pk=int(request.GET.get('item_id')))
            dataform = Itemsform(instance=pk)
        else:
            dataform = Itemsform()
    if atri == 'item_deleteform':
        if request.GET.get('item_id'):
            pk = Items.objects.get(pk=int(request.GET.get('item_id')))
            dataform = Itemsform(instance=pk)
        else:
            dataform = Itemsform()
    if atri == 'item_addform':
        dataform = Itemsform()
    if atri == 'addsent':
        if request.POST.get('oid'):
            dataform = consigneeform.objects.get('consignee')
    if atri == 'allparty' :
        if request.POST.get('party') == 'all':
            match=request.POST.get('selected')
            dataform = Clients.objects.all().order_by('party')
    if atri == 'allconsignee' :
        if request.POST.get('consignee') == 'all' and request.POST.get('party_id')!= None:
            match=request.POST.get('selected')
            dataform = Consignees.objects.filter(party_id=request.POST.get('party_id')).order_by('consignee')


    return render(request, 'form_data.html', {'form': dataform, 'atri': atri,})


def item_wise(request, filter):
    if request.user.is_authenticated:
        if filter == 'item_wise':
            items = Items.objects.all().order_by('item_name')
            data = {'item': items, 'filter': filter}
        if filter == 'date_wise':
            items = Items.objects.all()
            data = {'item': items, 'filter': filter}
    else:
        return HttpResponseRedirect('/')

    return render(request, 'itemwiseorders.html', data)


def itemwise_data(request, filter):
    if request.method == 'POST':
        if filter == 'item_wise':
            item1 = request.POST.get('item_id')
            items = Items.objects.filter(pk=int(item1))
            orders = Orders.objects.filter(item_id=item1).order_by('orderdate')
            con = Consignees.objects.all()
            party = Clients.objects.all()
            data = {'order': orders, 'item': items,
                    'consignees': con, 'partys': party, 'filter': filter}
        if filter == 'date_wise':
            items = Items.objects.all()
            orders = Orders.objects.all().order_by('orderdate').order_by('orderdate')
            con = Consignees.objects.all()
            party = Clients.objects.all()
            data = {'order': orders, 'item': items,
                    'consignees': con, 'partys': party, 'filter': filter}

    return render(request, 'itemwise_data.html', data)
