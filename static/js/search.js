  $('.select2').select2({    
    placeholder: "Select ...",    
    width:"100%",
    
    });

    $('.select2').on("select2:open", function(event) {
      $('input.select2-search__field').attr('placeholder', 'Search ...');
  })