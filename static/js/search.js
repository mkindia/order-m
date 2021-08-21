/*function myFunction() {
    
  if(document.getElementById("myDropdown").style.display=="block"){
      document.getElementById("myDropdown").style.display="none"
  }else{document.getElementById("myDropdown").style.display="block"}
};

function onInput() {
    var val = document.getElementById("input").value;
    var opts = document.getElementById('items').childNodes;
    for (var i = 0; i < opts.length; i++) {
      if (opts[i].value === val) {          
        value2send = document.querySelector("#items option[value='"+opts[i].value+"']").dataset.value;          
        document.getElementById("myDropdown").style.display="none";          
        document.querySelector('#showinput').value = opts[i].value;  
        document.getElementById('showinput').value2send=value2send;
        break;       
      };
    };
  }; */

  $('.select2').select2({    
    placeholder: "Select in",
    width:"100%",    
    });