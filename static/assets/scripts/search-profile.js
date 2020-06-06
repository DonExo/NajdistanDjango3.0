$(".search-profile .input-checkbox-switch label").on("click", function () {
    const sp_pk = $(this).prev().attr("name");

    $.ajax({
        type:"POST",
        url: `/sp/toggle/`,
        async: true,
        dataType: "json",
        data: {"sp_pk": sp_pk},
        success: function(response){
            console.log(response)
        },
        error: function(xhr, status, err) {
          console.log(err);
        },
        complete: function(){
        }
      });
});
