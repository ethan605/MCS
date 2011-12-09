/*
 * MCS User CP functions
 */

$(document).ready(function() {
	/*
	 * Change password
	 */
	$("#changepass-notice").dialog({
		autoOpen: false,
		modal: true,
		resizable: false,
		buttons: {
			"OK": function() {
				$(this).dialog("close");
				$(location).attr("href", "/");
			}
		}
	});
	$("#changepass-dialog").dialog({
		autoOpen: false,
		modal: true,
		resizable: false,
		width: 350
	});
	$("#changepass-button").click(function() {
		$("#changepass-dialog").dialog("open");
		return false;
	});
	$("#id_current_pass,#id_new_pass,#id_confirm_pass").addClass("required");
	$("#id_new_pass").attr("notEqualTo", "#id_current_pass").attr("minlength", "6");
	$("#id_confirm_pass").attr("equalTo", "#id_new_pass");
	function formValidate() {
		return $("#changepass-form").validate({
			errorClass: "text-error",
			validClass: "text-success",
			errorElement: "span",
			errorPlacement: function(error, element) {
				$("#changepass-form #error-show").html(error);
			}
		}).form();
	}
	$("#changepass-form").ajaxForm({
		type: "POST",
		dataType: "json",
		beforeSubmit: formValidate,
		success: function(data) {
			if (data.res_current_pass)
				$("#changepass-form #error-show").html(data.res_current_pass).show();
			else {
				$("#changepass-dialog").dialog("close");
				$("#changepass-notice").html("Your password has been updated<br />Please re-sign in to system").dialog("open");
			}
		}
	});
});