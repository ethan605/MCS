$(document).ready(function() {
	$("table,tr,td").addClass("noborder");
	$("#id_display_name,#id_address,#id_re_password").addClass("required");
	$("#signup-form #id_username").addClass("required lettersdigits");
	$("#signup-form #id_password").addClass("required").attr("minlength", "6");
	$("#id_re_password").attr("equalTo", "#id_password");
	$("#id_email,#id_re_email").addClass("required email");
	$("#id_re_email").attr("equalTo", "#id_email");
	$("#id_phone_number").addClass("required digits");

	$("#notice-dialog").dialog({
		title: "Signup notice",
		buttons: {
			"OK": function() { 
				$(this).dialog("close"); 
				$(location).attr("href", "/usercp/");
			}
		}
	});

	function formValidate() {
		return $("#signup-form").validate({
			errorClass: "text-error",
			validClass: "text-success",
			errorElement: "span",
			errorPlacement: function(error, element) {
				$("#signup-form #error-display").html(error);
			}
		}).form();
	}
	$("#signup-form").ajaxForm({
		dataType: "json",
		beforeSubmit: formValidate,
		success: function(data) {
			if (data.res_username != "")
				$("#error-display").html(data.res_username).show()
			else if (data.res_email != "")
				$("#error-display").html(data.res_email).show()
			else
				$("#notice-dialog").html("User's successfully registered").dialog("open");
		}
	});
});