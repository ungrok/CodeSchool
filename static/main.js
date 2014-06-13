$(document).ready(function () {
  console.log("ready");
  var $form = $("#the-form");

  $form.submit(function (e) {
    e.preventDefault();

    var formData = $form.serialize();
    console.log("the form data", formData);

    var url = "/signup";

    $.post(url, formData, function (data) {
	console.log("server", data);
	alert("Good job, " + data.first_name + "!");
    }).fail(function () {
      alert("Whoa! That didn't work, yo.");
    });
  });
});
