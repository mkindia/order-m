

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
    // for temalert box
    function tempAlert(msg,duration)
    {
     var el = document.createElement("div");
      
     el.setAttribute("style","font-size:22px;font-weight:bold;margin-left:15%;top:2px; border-radius:10px;color:black;border-color:#4385cc ; border-width:2px; border-style: solid; position:absolute;z-index:10000;width:70%;line-height:auto; background-color:#f2f6f8; text-align:center;");
     
     el.innerHTML = msg
     setTimeout(function(){
      el.parentNode.removeChild(el);
         },duration);
     document.body.appendChild(el);
    }
    // messsage time out box
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
        });
    }, 1000);

    //for search box
   
 if(window.location.pathname=='/'){
       // tempAlert("hrkkkh hjgd fjghj",5000);
        document.getElementById("consign").disabled=true;

        function showAjexOrder(pid,con)
        {   
                
            if(con == "All Consignee" && pid != "selectparty"  )
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
                 'conid': con
             },
             success: function (data) {
                 $("#orders").html(data);
             }
 
              });
 
        };
        };
    
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
            let pid=document.getElementById('consid').value;
            let con=document.getElementById('consign').value;
           if ( confirm("Are you sure to Delete this record ?"))
           {

            var id = $(this).attr("seid");

            $.ajax({
    
                type : "POST", 
                url: '/addsent/delete/',
                data: {
                    sid:id,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                
                },
                success: function (data) {
                          showAjexOrder(pid,con);  
                          alert('Delete Success');              
                   
                }
            })
            }         

        });

        // For Delete Consignee Order ordelete
        $("#ordertableid tbody").on('click', '#ordelete', function () {
            
            let pid=document.getElementById('consid').value;
            let con=document.getElementById('consign').value;
           // document.getElementById("sedelete").setAttribute('data-bs-dismiss',"modal");
            if ( confirm("Are you sure to Delete this Order ?"))
            {
 
                var id = $(this).attr("oid");                
                $.ajax({        
                    type : "POST", 
                    url: '/addorder/delete/',
                    data: {
                        oid:id,
                        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                        //action: 'POST'
                    },
                    success: function () {
                            showAjexOrder(pid,con);                           
                            alert('Order Delete Success');              
                        
                    }
                });
             }         
 
         });
        
 };
 
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

};
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
})};
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





};
// For Delete Consignee
if(window.location.pathname=='/editconsignee/delete/'){
        
    $("#partylist").change(function(){
      
        var partyid= $(this).val();
       
        if(partyid=="selectparty")
        {
            partyid=0;
        }
        $.ajax({
            
            url: '/con_data/fordeletecon/',
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

};
// For Edit Items
if(window.location.pathname=='/items/edit/'){

    $("#editbtn").click(function(){
        let selectvalue=document.getElementById('select2').value; 
       
       if(selectvalue!=null)
       {
        $.ajax({
    
            url: '/form_data/item_editform',
            data: {
                item_id: selectvalue,
            },
            success: function (data) {    
                      
                $("#form_data").html(data);
            },
            fail : function(){alert('Item Not Found')},
            error: function(){alert('page not found')}
        });
    }
    });
    

};
// For Delete Items
if(window.location.pathname=='/items/delete/'){
     
   
    $('#editbtn').click(function(){
        if( confirm("Delete This Item ?") )
   {
       let selectvalue=document.getElementById('select2').value;
      
        //var selectvalue= $(this).val();
        $.ajax({
            type : "POST", 
            url: '/items/delete/',
            data: {
                item_id: selectvalue,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {    
                      
                //$("#form_data").html(data);
                if (data.msg!='None'){alert('Can not delete item Exist In order (  '+data.msg+'  )')}
                if(data.msg=='None'){                    
                     alert('Item Delete Success');
                     //window.location.replace('/items/delete/');
                    }
            }
        });
    }
    });

};
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

};

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
   

};

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


   

};

if(window.location.pathname=='/addsent/add/'){
    $('#scon').hide()
    $('#docket_number').hide();
   // $('#id_docket_number').attr('required',true)
    //document.getElementById('select_Consignee').disabled=true;
    $("#id_status").change(function(){
       
        var selectvalue= $(this).val();
        if (selectvalue == 'Transfer To')
        {
            $('#select_Consignee').attr('required',true);            
            $('#scon').show();
         //document.getElementById('select_Consignee').disabled=false;           
        }
        else
        {
            $('#select_Consignee').attr('required',false);            
            $('#scon').hide();
            //document.getElementById('select_Consignee').disabled=true;
        }

        if(selectvalue == 'Delivered......')
        {    
            $('#id_docket_number').attr('required',true)
            $('#docket_number').hide();           
        }
        else
        {   $('#id_docket_number').attr('required',false)
            $('#docket_number').hide();
             
        }
        
    })    

};

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


};

if(window.location.pathname=='/addorder/add/'){
    document.getElementById("addorder2").disabled=true;
   
    $("#id_orderdate").change(function()
    {
        
        if(document.getElementById('id_orderdate').value != "" )
         {
        if(document.getElementById('consid').value != "")
        {
            document.getElementById('addorder2').disabled=false;
        }
        else(document.getElementById('addorder2').disabled=true)

         }
        else(document.getElementById('addorder2').disabled=true)
   
    });
    
    // For select party and get consignee
    $("#consid").change(function()
    {
            
        if(document.getElementById('consid').value != "" )
        {
        if(document.getElementById('id_orderdate').value != "")
        {
            document.getElementById('addorder2').disabled=false;
        }
        else(document.getElementById('addorder2').disabled=true)
        }
         else(document.getElementById('addorder2').disabled=true)
     
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
   
   
    $("#addorder").on('click', function () {        
        info=[];
        let party_id=document.getElementById("consid").value;
        let con_id=document.getElementById("consign").value;
        let id_orderdate=document.getElementById("id_orderdate").value;
        let comment = null; 
        if(document.getElementById("id_comment").value != ""){comment=document.getElementById("id_comment").value};
        
       // let item_id=document.getElementById('showinput').value2send;
       // let item=document.getElementById('showinput').value;
       // let item=document.getElementById('select2');
        let item_id=document.getElementById('select2').value;
       // alert(item.value +" "+item.options[item.selectedIndex].text)
        let item_des = $("#id_item_des").val();
        let qty = $("#id_qty").val();
        let unit = $("#id_unit").val();
        let price = document.getElementById('id_item_price').value;
        let per = document.getElementById('id_per').value;      
        let item_des1 = null;
               
         if(item_des != ""){item_des= item_des,item_des1="("+item_des+")" };
       
    if(item_id != null)
    { 
        if(qty != "")
        {  
            if(unit != "")
            {   
                if(price != "")
                {
                    info.push(party_id,con_id,id_orderdate,item_id,item_des,qty,unit,price,comment,per);

                    $.ajax({        
                        type : "POST",
                        url: '/addorder/add/',
                        data: {'info[]':info,
                            
                            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                            // action: 'POST'
                            
                        },
                        success: function (database) {
                            $('#select2').val(null).trigger('change');                                   
                              // document.getElementById("input").value=null;
                                var x2=document.getElementById("id_item_des");       
                                    x2.value=null;

                                var qtyval=document.getElementById("id_qty");
                                qtyval.value=null;

                                    var priceval=document.getElementById("id_item_price");
                                    priceval.value=null;

                                //window.setTimeout('alert("Order Item Success");',100);              
                                tempAlert("add Item Order Success",1500)
                        }
                    });
                }
                else(alert("Please Enter Price"));

            }
            else(alert("Please Select unit"));

        }
        else(alert("Please Enter Qty."));

    }
    else(alert("Please Select Item"));

     
    });

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
               // var lastitem=data.sitem;
                //        alert(lastitem); 
                
                $.ajax({
    
                    url: '/items_data/',
                    data: {
                        'item_id': null
                    },
                    success: function (data) {
                    
                     $("#select2").html(data);
                     tempAlert("item added success please select",1500);
                    }
                });
                
            }            
        });
        
    })
   

};


});