

$(document).ready(function(){$("#consign").change(function () {

   // var url = $("#consigneeselect").attr("con-url");
    
    var currow =  $(this).val();
    // var currow=$(this).attr('sat');
    // var col1 = currow.find('td:eq(0)').text();
   // alert(url)
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


$("#ordertableid tbody").on('click', '#sentdetailbtn', function () {

   // var url = $("#sentdetailform").attr("sentdetail-url");
   
    //var url="sent_data"
    var id = $(this).attr("atb");
  
    // var currow=$(this).attr('sat');
    // var col1 = currow.find('td:eq(0)').text();
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


// for addorder item_data for id id_tem_name
if (window.location.pathname == '/addorder/'){
    $.ajax({
            
        url: '/item_data/',
        data:{
            'id':0
        },
        success:function(data) {
          
            $("#id_item_name").html(data);
    
        }}); 
 }
// For Edit Party
if(window.location.pathname=='/editparty/edit/'){$("#partylist").change(function(){
    alert('');
    var selectvalue= $(this).val();
    $.ajax({

        url: '/form_data/party_editform',
        data: {
            'partyid': selectvalue
        },
        success: function (data) {    
                   alert(selectvalue);
            $("#form_data").html(data);
        }
    })
})}
// For Delete Party
if(window.location.pathname=='/editparty/delete/'){$("#partylist").change(function(){
    alert('');
    var selectvalue= $(this).val();
    $.ajax({

        url: '/form_data/party_deleteform',
        data: {
            'partyid': selectvalue
        },
        success: function (data) {    
                   alert(selectvalue);
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
                   alert(selectvalue);
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
                   alert(selectvalue);
            $("#form_data").html(data);
        }
    })

   });

}
 
 //for edit party
/*$("#editparty").click(function(){
    alert('Hello');
    $('#editformaction').attr('action','party/edit/')
})

$("#deleteparty").click(function(){
    alert('Hello');
   // $('#btnaction').attr('value','Delete')
    $('#editformaction').attr('action','party/delete/')
})*/

 // for home page and orders
$("#consid").change(function(){

   // var url = $("#confind").attr("con-url");
    var programingId= $(this).val();
    var orderid = 0;
   // alert(url)
    if(programingId == "selectparty")
    {


        programingId=0;

    }

   
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

    }); });    


});