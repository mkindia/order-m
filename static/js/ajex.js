

$(document).ready(function(){

    // auto hde navbar
    $(window).on('click', function(event){
        // element over which click was made
        var clickOver = $(event.target)
        if ($('.navbar .navbar-toggler').attr('aria-expanded') == 'true' && clickOver.closest('.navbar').length === 0) {
            // Click on navbar toggler button
            $('button[aria-expanded="true"]').click();
        }
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
if(window.location.pathname=='/editparty/delete/'){$("#partylist").change(function(){
    
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
 
 
 


});