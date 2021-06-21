

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

       // For select party
       $("#consid").change(function()
       {
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
                   'conid': orderid
               },
               success: function (data) {    
                       
                   $("#orders").html(data);
               }

           });

       // for connsignees
           
           $.ajax({
                   
               url: '/con_data/',
               data:{
                   'cons1':programingId
               },
               success:function(data) {
               
                   $("#consign").html(data);

               }

           });

       });  
       

           // change party and consignee
       $("#consign").change(function () {   
           
           var currow =  $(this).val();
           
           if(currow != "Select Consignee")
           {
               
           //  document.getElementById("navconsignee").disabled=false;
           }
           else
           {
           //  document.getElementById('navconsignee').disabled=true;
               currow=0;
           }
           
           $.ajax({

               url: '/for_data/',
               data: {
                   'conid': currow
               },
               success: function (data) {
                   $("#orders").html(data);
               }

           });


           
       });


 // For home
 if(window.location.pathname=='/'){
                
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

if(window.location.pathname=='/itemwiseorders/'){

    $("#select_item").change(function(){
    
        var selectvalue= $(this).val();
       
        $.ajax({
    
            type : "POST", 
            url: '/itemwise_data/',
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

    })
   

}

if(window.location.pathname=='/addsent/add/'){
    $('#scon').hide()
    //document.getElementById('select_Consignee').disabled=true;
    $("#id_status").change(function(){
       
        var selectvalue= $(this).val();
        if (selectvalue == 'Transfer To Consignee')
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


});