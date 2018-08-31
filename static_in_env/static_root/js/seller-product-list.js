$(function () {

  /* Functions */
  var loadForm = function () {
    var btn = $(this);
    var dktp_list_display = $(".seller-product-list").children("#dktp-seller-product-list").css("display");
    $.ajax({
      url: btn.attr("data-url"),
      data: {
        'dktp_list_display':dktp_list_display
      },
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-product .modal-content").html("");
        $("#modal-product").modal("show");
      },
      success: function (data) {
        $("#modal-product .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    var formData = new FormData(this);
    $.ajax({
      url: form.attr("action"),
      data: formData,
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $(data.list_selector).html(data.html_product_list);
          $("#modal-product").modal("hide");
        }
        else {
          $("#modal-product .modal-content").html(data.html_form);
        }
      },
      cache: false,
      contentType: false,
      processData: false
    });
    // "false" prevents the browser to perform a full HTTP POST to the server
    return false;
  };


  // Create product
  $(".js-create-product").click(loadForm);
  $("#modal-product").on("submit", ".js-product-create-form", saveForm);

  // Update product
  $(".seller-product-list").on("click", ".js-update-product", loadForm);
  $("#modal-product").on("submit", ".js-product-update-form", saveForm);

  // Delete book
  $(".seller-product-list").on("click", ".js-delete-product", loadForm);
  $("#modal-product").on("submit", ".js-product-delete-form", saveForm);
});