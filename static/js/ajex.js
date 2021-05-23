

$(document).ready(function(){
   
    //alert('hello');
    
  //document.getElementById('navconsignee').disabled=true;
 // document.getElementById('consign').disabled=true;
 // document.getElementById('navaddorders').disabled=true;

$("#consign").change(function () {

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
else if(window.location.pathname == '/alert.php'){
     $("#mytextfield").hover()
     {
       alert('message');
     }
 }


// for home page and orders
$("#consid").change(function(){

   // var url = $("#confind").attr("con-url");
    var programingId= $(this).val();
    var orderid = 0;
   // alert(url)
    if(programingId != "selectparty")
    {

       // document.getElementById("add_orders").disabled=false;
    //  document.getElementById('consign').disabled=false;
    }
    else
    {
      //  document.getElementById('add_orders').disabled=true;
       // document.getElementById('consign').disabled=true;
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

    }); 
    

     

});    






});