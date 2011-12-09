/*
 * MCS User sign in & sign out functions
 */

$(document).ready(function() {
	/*
	 * Sign in
	 */
	$("#signin-notice").dialog({
		autoOpen: false,
		modal: true,
		resizable: false,
		buttons: {
			"OK": function() { 
				$(this).dialog("close"); 
				if ($(this).html() == "User authenticated")
					$(location).attr("href", "/");
			}
		}
	});
	$("#signin-dialog").dialog({
		autoOpen: false,
		modal: true,
		resizable: false,
	});
	$("a#signin-button").click(function() {
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
		type: "POST",
		dataType: "json",
		beforeSubmit: formValidate,
		success: function(data) {
			$("#signin-form #error-show").html(data.res_username + data.res_password).show();
			if (data.res_result) {
				$("#signin-notice").html(data.res_result).dialog("open");
				if (data.res_result == "User authenticated")
					$("#signin-dialog").dialog("close");
			}
		}
	});

	/*
	 * Sign out
	 */
	$("#signout-confirm").dialog({
		autoOpen: false,
		modal: true,
		resizable: false,
		buttons: {
			"OK": function() {
				$.ajax({
					type: "POST",
					url: "/signout/",
					success: function(data) {
						$("#signout-confirm").dialog("close");
						$("#signout-notice").html("You're successfully signed out!").dialog("open");
					}
				});
			},
			"Cancel": function() {
				$(this).dialog("close");
			}
		}
	});
	$("#signout-notice").dialog({
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
	$("#signout-button").click(function() {
		$("#signout-confirm").html("Are you really want to sign out?").dialog("open");
		return false;
	});
});