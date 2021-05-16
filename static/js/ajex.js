

$(document).ready(function(){
   
    
document.getElementById('add_consignee').disabled=true;

$("#consi2 tbody").on('click', '#sho', function () {

    var url = $("#indexForm").attr("data-url");

    var currow = $(this).attr("sat");
    // var currow=$(this).attr('sat');
    // var col1 = currow.find('td:eq(0)').text();
    
    $.ajax({

        url: url,
        data: {
            'conid': currow
        },
        success: function (data) {
            $("#orders").html(data);
        }

    });


       
});


$("#ordertableid tbody").on('click', '#sentdetailbtn', function () {

    var url = $("#sentdetailform").attr("sentdetail-url");
   
    //var url="sent_data"
    var id = $(this).attr("atb");
  
    // var currow=$(this).attr('sat');
    // var col1 = currow.find('td:eq(0)').text();
    $.ajax({

        url: url,
        data: {
            'orderid': id
        },
        success: function (data) {
            $("#sentdetaildata").html(data);
        }

    });

});


$("#consid").change(function(){

    var url = $("#confind").attr("con-url");
    var programingId= $(this).val();
    
    if(programingId != "selectparty")
    {
        
        document.getElementById("add_consignee").disabled=false;
    }
    else
    {
        document.getElementById('add_consignee').disabled=true;
    }

    // for clear orders
    url2="/for_data/";
     var orderid = 0;
    //alert(url)
    $.ajax({

        url: url2,
        data: {
            'orderid': orderid
        },
        success: function (data) {    
                   
            $("#orders").html(data);
        }

    });

// for connsignees
      
    $.ajax({

        url: url,
        data:{
            'cons1':programingId
        },
        success:function(data) {
            
            $("#consign").html(data);

        }

    }); 
    

     

});    






});