$(".search-profile .input-checkbox-switch label").on("click", function () {
    const switchId = $(this).prev().attr("id");
    const switchPk = $(this).prev().attr("name");

    $.ajax({
        type:"POST",
        url: `sp/toggle-status`,
        async: true,
        dataType: "json",
        data: {"spPk": switchPk}, 
        success: function(response){

        },
        error: function(xhr, status, err) {
          console.log(err);
        },
        complete: function(){
          console.log('finished');
        }
      });
});