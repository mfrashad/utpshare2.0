$(function(){
  $(".js-show-sale-detail").click(function(e){
    e.preventDefault();
    var link = $(this);
    $.ajax({
      url: link.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-sale .modal-content").html("");
        $("#modal-sale").modal("show");
      },
      success: function (data) {
        $("#modal-sale .modal-content").html(data.sale_detail_template);
      }
    });
  });

  $(".js-approve-order").click(function(e){
    e.preventDefault();
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        $(".sale-status-" + data.sale_id).text(data.new_sale_status);
        $(btn).hide();
      }
    });
  });

});