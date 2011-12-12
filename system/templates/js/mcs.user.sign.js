/*
 * MCS User sign in & sign out functions
 */

$(document).ready(function() {
	/*
	 * Sign in
	 */
	$("[id=signin-button]").click(function() {
		$("#signin-dialog").dialog("open");
		return false;
	});
	$("#signin-form #id_username,#signin-form #id_password").addClass("required");
	function formValidate() {
		return $("#signin-form").validate({
			errorClass: "text-error",
			validClass: "text-success",
			errorElement: "span",
			errorPlacement: function(error, element) {
				$("#signin-form #error-show").html(error);
			}
		}).form();
	}
	$("#signin-form").ajaxForm({
		dataType: "json",
		beforeSubmit: formValidate,
		success: function(data) {
			$("#signin-form #error-show").html(data.res_username + data.res_password).show();
			if (data.res_result) {
				if (data.res_result == "User authenticated") {
					$("#signin-dialog").dialog("close");
					$(location).attr("href", "/");
				}
				else
					$("#notice-dialog").html(data.res_result).dialog("open");
			}
		}
	});

	/*
	 * Sign out
	 */
	$("#signout-button").click(function() {
		$("#signout-dialog").html("Are you really want to sign out?").dialog("open");
		return false;
	});
	$("#signout-dialog").dialog({
		autoOpen: false,
		buttons: {
			"OK": function() {
				$.ajax({
					type: "POST",
					url: "/signout/",
					success: function(data) {
						if (data == "") {
							$("#signout-confirm-dialog").dialog("close");
							$(location).attr("href", "/");
						}
					}
				});
			},
			"Cancel": function() {
				$(this).dialog("close");
			}
		}
	});
});