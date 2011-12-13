/*
 * MCS User CP functions
 */

$(document).ready(function() {
	$("table,tr,td").addClass("noborder");
	/*
	 * Change password
	 */
	$("#change-password-notice").dialog({
		buttons: {
			"OK": function() {
				$(this).dialog("close");
				$(location).attr("href", "/");
			}
		}
	});
	$("#changepass-button").click(function() {
		$("#change-password-dialog").dialog("open");
		return false;
	});
	$("#id_current_pass,#id_new_pass,#id_confirm_pass").addClass("required");
	$("#id_new_pass").attr("notEqualTo", "#id_current_pass").attr("minlength", "6");
	$("#id_confirm_pass").attr("equalTo", "#id_new_pass");
	function formValidate() {
		return $("#change-password-form").validate({
			errorClass: "text-error",
			validClass: "text-success",
			errorElement: "span",
			errorPlacement: function(error, element) {
				$("#change-password-form #error-show").html(error);
			}
		}).form();
	}
	$("#change-password-form").ajaxForm({
		dataType: "json",
		beforeSubmit: formValidate,
		success: function(data) {
			if (data.res_current_pass)
				$("#change-password-form #error-show").html(data.res_current_pass).show();
			else {
				$("#change-password-dialog").dialog("close");
				$("#change-password-notice").html("Your password has been updated<br />Please re-sign in to system").dialog("open");
			}
		}
	});
});