
$(document).ready(function(){
 
  //Enter Only Values calculation  
   $("body").delegate(".qty","keyup",function(event){
    event.preventDefault();
    var row = $(this).parent().parent();
    var weight = row.find('.wgt').val();
    var qty = row.find('.qty').val();
   
    var total = 0;
    if(isNaN(qty)) {
      qty = 1;
    };
    if (qty < 1) {
      qty = 1;
    };
    var total = parseInt(weight) * parseInt(qty);
  

    row.find('.total').val(total);
    row.find('.subtotal').val(total);
    var net_total=0;
    $('.subtotal').each(function(){
      net_total += ($(this).val()-0);
    })
    $('.net_total').html("Total :  " +net_total+"&nbsp;Kg");
    $('#ntotal').val(net_total); 

    var total_caret = 0;
    $('.qty').each(function(){
      total_caret += ($(this).val()-0);
    })

    palacaret = $("#caretqty").val();
    var caretsum = 0;
    caretsum = parseInt(total_caret) + parseInt(palacaret);
    $('.total_caret').html("No Of Caret :  " +caretsum);
    $('#finalcaret').val(caretsum);

  })

   

   //Extra goods Calculation
   $("body").delegate(".ext","keyup",function(event){
    event.preventDefault();
    var row = $(this).parent().parent();
    var extra = row.find('.ext').val();
    var exttotal = row.find('.total').val();

    var finaltotal = 0;
    if(extra > 0){
    var finaltotal = parseFloat(extra) + parseFloat(exttotal);
    row.find('.subtotal').val(finaltotal.toFixed(2));
    var net_total=0;

    $('.subtotal').each(function(){
      net_total += ($(this).val()-0);
    })

    $('.net_total').html("Total : " +net_total.toFixed(2)+"&nbsp;Kg");
    $('#ntotal').val(net_total.toFixed(2));
  }else{
    row.find('.subtotal').val(exttotal.toFixed(2));
  }

})


//click rate calculate total amount of goods
$("body").delegate(".frate","keyup",function(event){
  var row = $(this).parent().parent();
  var totalkg = row.find('.subtotal').val();
  var rate = row.find('.frate').val();
  var palabill = $("#palabill").val();


  var finalamount = parseFloat(totalkg) * parseFloat(rate);
  row.find('.finaltotal').val(finalamount.toFixed(2));
  var nettotal = 0;
  $('.finaltotal').each(function(){
      nettotal += ($(this).val()-0);
    })

    total = parseFloat(nettotal) + parseFloat(palabill);
  $('.bill').html("Total Rs: " +total.toFixed(2));
 
  $('#fbill').val(total.toFixed(2));

});


   //chnage pala auto chnage final amt
  $("body").delegate(".pala","keyup",function(event){
    event.preventDefault();

    var cqty = $("#caretqty").val();
    var prate = $("#palarate").val();
    var pbill = 0;
    if(prate>0 && cqty > 0){
      pbill = parseInt(cqty) * parseFloat(prate);
    }

    if(isNaN(pbill)){      
      pbill=0;
      $("#palabill").val(pbill.toFixed(2));
    }else{
      $("#palabill").val(pbill.toFixed(2));
    }

    var palabill = $("#palabill").val();
    var stotal = $("#fbill").val();

    if(palabill>0){
      var bill = 0;
      bill = parseFloat(palabill) + parseFloat(stotal);
      $('.bill').html("Total Rs: " +bill.toFixed(2));
      $('#grandtotal').val(bill.toFixed(2));
    }

});

  //change pala qty auto chnage all fields
  $("body").delegate(".cqty","keyup",function(event){
    event.preventDefault();

    var cqty = $("#caretqty").val();
    var prate = $("#palarate").val();
    var caret = $("#finalcaret").val();
    var total = $("#fbill").val();

    totalcaret = parseInt(cqty) + parseInt(caret);
    if(isNaN(totalcaret)){
      $('.total_caret').html("No Of Caret :  " +caret);
    }else{
      $('.total_caret').html("No Of Caret :  " +totalcaret);
    }
   
    var pbill = 0;
 
    pbill = parseFloat(prate) * parseFloat(cqty);
    
    if(isNaN(pbill)){      
      pbill=0;
      $("#palabill").val(pbill);
    }else{
      $("#palabill").val(pbill);
    }
    var bill = 0;
    
    bill = parseFloat(pbill) + parseFloat(total);
    
    $('.bill').html("Total Rs: " +bill.toFixed(2));
    $('#grandtotal').val(bill.toFixed(2));

	});
});