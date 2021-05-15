

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


    $.ajax({

        url: url="sentform",
        data: {
            'orderid': currow
        },
        success: function (data) {
            $("#sentdetaildata").html(data);
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

      
    $.ajax({

        url: url,
        data:{
            'cons1':programingId
        },
        success:function(data) {
            
            $("#consign").html(data);

        }

    });     
    

    //for sent refresh
    alert(programingId)
    
    $.ajax({

        url: url,
        data: {
            'orderid': programingId
        },
        success: function (data) {
            $("#sentdetaildata").html(data);
        }

    });


});    






});