

$(document).ready(function(){

    // auto hide navbar
    $(window).on('click', function(event){
        // element over which click was made
        var clickOver = $(event.target)
        if ($('.navbar .navbar-toggler').attr('aria-expanded') == 'true' && clickOver.closest('.navbar').length === 0) {
            // Click on navbar toggler button
            $('button[aria-expanded="true"]').click();
        }
    });

    function tempAlert(msg,duration)
    {
     var el = document.createElement("div");
      
     el.setAttribute("style","border-radius:10px;margin-left:10%;color:white; position:absolute;z-index:10000;top:45%;width:80%;line-height: 80px; background-color:#262626; text-align:center;");
     
     el.innerHTML = msg
     setTimeout(function(){
      el.parentNode.removeChild(el);
         },duration);
     document.body.appendChild(el);
    }

    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
        });
    }, 1000);
      
  //  tempAlert("Order Added Success",2000);
 // For home
 if(window.location.pathname=='/'){

        document.getElementById("consign").disabled=true;

         // For select party
       $("#consid").change(function()
       {
           if(document.getElementById("consid").value != "selectparty")
           {
            document.getElementById("consign").disabled=false;
                    var programingId= $(this).val();
                    var orderid = 0;
                // alert(url)
                    if(programingId == "selectparty")
                    { programingId=0; }

                
                    // for clear orders
                    url2="/for_data/";   
                
                    $.ajax({

                        url: url2,
                        data: {
                            'pid': programingId
                        },
                        success: function (data) {    
                                
                            $("#orders").html(data);
                        }

                    });

                // for featch connsignees
                    
                    $.ajax({
                            
                        url: '/con_data/forhome/',
                        data:{
                            'cons1':programingId
                        },
                        success:function(data) {
                        
                            $("#consign").html(data);

                        }

                    });
        }
        else
        {
            document.getElementById("consign").disabled=true;
        }

       });  
       

           // change party and consignee
       $("#consign").change(function () {   
           
           var currow =  $(this).val();
           var pid= document.getElementById("consid").value;
           if(currow == "All Consignee" && pid != "selectparty"  )
           {
             
           //  document.getElementById("navconsignee").disabled=false;
           
           url2="/for_data/";   
   
       $.ajax({

           url: url2,
           data: {
               'pid': pid
           },
           success: function (data) {    
                   
               $("#orders").html(data);
           }

       });
           }
           else
           {
           //  document.getElementById('navconsignee').disabled=true;              
           $.ajax({

            url: '/for_data/',
            data: {
                'conid': currow
            },
            success: function (data) {
                $("#orders").html(data);
            }

        });

               
           }
         
         

           
       });

                
        // For show sent item
        $("#ordertableid tbody").on('click', '#sentdetailbtn', function () {

            var id = $(this).attr("atb");
            $.ajax({

                url: '/sent_data/',
                data: {
                    'orderid': id
                },
                success: function (data) {
                    $("#sentdetaildata").html(data);
                }

            });

        });
      
        // For Delete sent data
        $("#sentdetailtable tbody").on('click', '#sedelete', function () {

           if ( confirm("Are you sure to Delete this record ?"))
           {

            var id = $(this).attr("seid");

            $.ajax({
    
                type : "POST", 
                url: '/addsent/delete/',
                data: {
                    sid:id,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'POST'
                },
                success: function (data) {    
                          alert('Delete Success')                   
                   
                }
            })
            }         

        });

        // For Delete Consignee Order
        $("#ordertableid tbody").on('click', '#ordelete', function () {

            if ( confirm("Are you sure to Delete this Order ?"))
            {
 
                var id = $(this).attr("oid");                
                $.ajax({        
                    type : "POST", 
                    url: '/addorder/delete/',
                    data: {
                        oid:id,                         
                        dataType: "json",
                        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                        action: 'POST'
                    },
                    success: function (data) {    
                            alert('Delete Success')                   
                        
                    }
                })
             }         
 
         });
        
 }
 
 // For edit party
if(window.location.pathname=='/editparty/edit/'){
    
    $("#partylist").change(function(){   
    var selectvalue= $(this).val();
    $.ajax({

        url: '/form_data/party_editform',
        data: {
            'partyid': selectvalue
        },
        success: function (data) {    
                  
            $("#form_data").html(data);
        }
    })
})

}
// For Delete Party
if(window.location.pathname=='/editparty/delete/'){
    $("#partylist").change(function(){
    
    var selectvalue= $(this).val();
    $.ajax({

        url: '/form_data/party_deleteform',
        data: {
            'partyid': selectvalue
        },
        success: function (data) {    
                   
            $("#form_data").html(data);
        }
    })
})}
// For Edit Consignee
if(window.location.pathname=='/editconsignee/edit/'){
  
    $("#partylist").change(function(){
        var partyid= $(this).val();
       
        if(partyid=="selectparty")
        {
            partyid=0;
        }
        $.ajax({
            
            url: '/con_data/foreditcon/',
            data:{
                'cons1':partyid
            },
            success:function(data) {               
                $("#consigneelist").html(data);                    
            }    
        });
       
    });


    $("#consigneelist").change(function(){
    
    var selectvalue= $(this).val();
  
    $.ajax({

        url: '/form_data/consignee_editform',
        data: {
            'conid': selectvalue
        },
        success: function (data) {    
                   
            $("#form_data").html(data);
        }
    })

   });





}
// For Delete Consignee
if(window.location.pathname=='/editconsignee/delete/'){

    $("#partylist").change(function(){
        var partyid= $(this).val();
       
        if(partyid=="selectparty")
        {
            partyid=0;
        }
        $.ajax({
            
            url: '/con_data/',
            data:{
                'cons1':partyid
            },
            success:function(data) {               
                $("#consigneelist").html(data);                    
            }    
        });
       
    });


    $("#consigneelist").change(function(){
    
    var selectvalue= $(this).val();
  
    $.ajax({

        url: '/form_data/consignee_deleteform',
        data: {
            'conid': selectvalue
        },
        success: function (data) {    

            $("#form_data").html(data);
        }
    })

   });

}
// For Edit Items
if(window.location.pathname=='/items/edit/'){
    
    $("#select_item").change(function(){
       
        var selectvalue= $(this).val();
        $.ajax({
    
            url: '/form_data/item_editform',
            data: {
                'item_id': selectvalue
            },
            success: function (data) {    
                      
                $("#form_data").html(data);
            }
        })
    })


}
// For Delete Items
if(window.location.pathname=='/items/delete/'){
    
    $("#select_item").change(function(){
       
        var selectvalue= $(this).val();
        $.ajax({
    
            url: '/form_data/item_deleteform',
            data: {
                'item_id': selectvalue
            },
            success: function (data) {    
                      
                $("#form_data").html(data);
            }
        })
    })

    $("#form_data").on('click', '#itemdel', function () {

        var id = $('#select_item').val();
        $.ajax({

            type : "POST", 
            url: '/items/delete/',
            data: {
                item_id:id,
             //item_name : $('#select_item').val(),
             //last_name : $('#last_name').val(),
             //csrfmiddlewaretoken: '{{ csrf_token }}',                 
             dataType: "json",
             csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
             action: 'post'
     
            },
            
            success: function(data){
              
                if (data.msg!='None'){alert('Can not delete item Exist In order (  '+data.msg+'  )')}
                if(data.msg=='None'){
                     window.location.replace('/');
                     alert('Item Delete Success');
                    }
                   
               //$('#form_data').html(data.msg) /* response message */      
               //       
              
            },
     
            failure: function() {
                alert('Fail')
            } 
        });

    });

}
// For item add
if(window.location.pathname=='/items/add/'){
        
    $.ajax({
    
        url: '/form_data/item_addform',
        data: {
            'item_id': 'None'
        },
        success: function (data) {
           
            $("#form_data").html(data);
        }
    })

}

if(window.location.pathname=='/itemwiseorders/item_wise/'){

    $("#select_item").change(function(){
    
        var selectvalue= $(this).val();
       if (selectvalue=="sdwo")
       {
        $.ajax({
    
            type : "POST", 
            url: '/itemwise_data/date_wise/',
            data: {
                item_id:selectvalue,                         
                dataType: "json",
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function (data) {    
                      
                $("#from_itemwise_data").html(data);
               
            }
        })
       
    }
    else if (selectvalue != "so") 
    {
        $.ajax({
    
            type : "POST", 
            url: '/itemwise_data/item_wise/',
            data: {
                item_id:selectvalue,                         
                dataType: "json",
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function (data) {    
                      
                $("#from_itemwise_data").html(data);
               
            }
        })
    }

    })
   

}

if(window.location.pathname=='/itemwiseorders/date_wise/'){

   
        $.ajax({
    
            type : "POST", 
            url: '/itemwise_data/date_wise/',
            data: {
                item_id:selectvalue,                         
                dataType: "json",
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function (data) {    
                      alert('success')
                $("#from_itemwise_data").html(data);
               
            }
        })


   

}

if(window.location.pathname=='/addsent/add/'){
    $('#scon').hide()
    //document.getElementById('select_Consignee').disabled=true;
    $("#id_status").change(function(){
       
        var selectvalue= $(this).val();
        if (selectvalue == 'Transfer To')
        {
            $('#select_Consignee').attr('required',true);
            
            $('#scon').show()
         //document.getElementById('select_Consignee').disabled=false;           
        }
        else
        {
            $('#select_Consignee').attr('required',false);
            $('#scon').hide()
            //document.getElementById('select_Consignee').disabled=true;
        }
        
    })    

}

if(window.location.pathname=='/addsent/edit/'){

    var status =$('#id_status').val()    
    if (status == 'Transfer To')
    {
        $('#select_Consignee').attr('required',true);        
        $('#scon').show()            
    }
    else
        {
            $('#select_Consignee').attr('required',false);
            $('#scon').hide()            
        }

        $("#id_status").change(function(){
       
            var selectvalue= $(this).val();
            if (selectvalue == 'Transfer To')
            {
                $('#select_Consignee').attr('required',true);                
                $('#scon').show()                    
            }
            else
            {
                $('#select_Consignee').attr('required',false);
                $('#scon').hide()                
            }
            
        })    


}

if(window.location.pathname=='/addorder/add/'){
    
   
    // For select party and get consignee
    $("#consid").change(function()
    {
     
             var programingId= $(this).val();
            
             $.ajax({
                            
                url: '/con_data/fororder/',
                data:{
                    'cons1':programingId
                },
                success:function(data) {
                
                    $("#consign").html(data);
        
                }
        
            });
    });
   
   
    // for add table row dynamicaly
    var count=0
    $("#addorder").on('click', function () {
        var valid = 0
        var iw = document.getElementById("item_name");
        var item_id=iw.value;
        var item=iw.options[iw.selectedIndex].text;

        var item_des = $("#id_item_des").val();
        var qty = $("#id_qty").val();
        var unit = $("#id_unit").val();
        var price = $("#id_item_price").val();
        var item_des1=""
        if(item != "Select Item"){ valid=valid+1}
         if(qty != ""){ valid=valid+1}
         if(unit != ""){ valid=valid+1}
         if(price != ""){ valid=valid+1}
         if(item_des != ""){item_des= item_des,item_des1="("+item_des+")" }
         
        if(valid==4)
        {
         if (count !=10) // add row
        {
        $("#items").append('<tr><td style="display:none;">'+item_id+'</td><td>'+ item + item_des1 +'</td><td style="display:none;">'+ item_des +'</td><td>'+ qty +'</td><td>'+unit+'</td><td>'+price+'</td><td><button class="btn-close" id="delrow" type="button"  > </button></td></tr>');
        count = count+1
        }else{alert("Only 10 Items add")}
         }
         else{alert("Enter item , Qty , Price")}
         
        var x=document.getElementById("item_name");       
        x.selectedIndex=0;

        var x=document.getElementById("id_item_des");       
        x.value=null

        var qtyval=document.getElementById("id_qty");
        qtyval.value=null

        var priceval=document.getElementById("id_item_price");
        priceval.value=null
        
        

    });
    //Remove table row
    $('#ordertableid').on('click', '#delrow', function () {
        $(this).closest('tr').remove();
        count=count-1
    })

    
    // For Save item to database
    $("#saveorders").on('click', function () {
        info=[];
        d=[];
        var n1 = document.getElementById("ordertableid").rows.length;
        var party_id=document.getElementById('consid').value
        var con_id=document.getElementById('consign').value;
        var id_orderdate=document.getElementById('id_orderdate').value;
        
        if(party_id != "" && con_id != "" && id_orderdate != "")
        {
            if(n1 >1)
       {
        for(i=1; i<n1;i++){
         
            var item_id=document.getElementById("ordertableid").rows[i].cells.item(0).innerHTML;
            var item=document.getElementById("ordertableid").rows[i].cells.item(1).innerHTML;
            var item_des=document.getElementById("ordertableid").rows[i].cells.item(2).innerHTML;
            var qty=document.getElementById("ordertableid").rows[i].cells.item(3).innerHTML;
            var unit=document.getElementById("ordertableid").rows[i].cells.item(4).innerHTML;
            var price=document.getElementById("ordertableid").rows[i].cells.item(5).innerHTML;
           
            info.push(party_id,con_id,id_orderdate,item_id,item_des,qty,unit,price);
        }
        $.ajax({        
            type : "POST",
            url: '/addorder/add/',
            data: {'info[]':info,
               
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
               // action: 'POST'
               
            },
            success: function (database) {    
                    window.setTimeout('alert("Order Item Success");location.reload(true); window.close();' , 100);              
                   
            }
        });
       
       // alert(info[0][3])
       // tempAlert("Order Added Success",2000);
        //w
       
        }
        else{alert('Plese add Order Frist')}
        }
        else{ alert('Please Select Party, Consignee, and Date') }
        
        
        
    })

    $("#additem").on('click', function () {
        var itemname = document.getElementById("add_item")
        
        $.ajax({        
            type : "POST", 
            url: '/items/add/',
            data: {
                         
                item_name:itemname.value,               
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'POST'
                
            },
            success: function (data) { 
                $.ajax({
    
                    url: '/items_data/',
                    data: {
                        'item_id': null
                    },
                    success: function (data) {    
                              
                        $("#item_name").html(data);
                        
                    }
                })             
                 
                
            }            
        });
        
    })
   

}


});