/*
 * MCS Admin functions
 */
$(document).ready(function() {
	$("#tabs").tabs();
	/*
	 * Init elements
	 * Buttons
	 *
	 * Status set buttons
	 */
	$(".set-status").each(function(i, e) {
		$(e).text($(e).attr("mode")=="True" ? "Deactivate":"Activate");
		$(e).click(function() {
			$("#set-status-dialog").attr("mode", $(e).attr("mode"))
				.attr("set-status-for", $(e).attr("id"))
				.html("Do you really want to " + ($(e).attr("mode")=="True" ? "deactivate":"activate") + " this user?")
				.dialog("open");
			return false;
		});
	});

	/*
	 * Checkboxes
	 */
	$("input#check-all").click(function() {
		if ($(this).is(":checked"))
			$("input.check:not(:checked)").attr("checked", "checked")
		else
			$("input.check:checked").removeAttr("checked");
	});
	
	/*
	 * Set multi status button
	 */
	$(".change-multi.status").click(function() {
		if ($("input.check:checked").length > 0) {
			$("#set-multi-status-dialog #activate").click();
			$("#set-multi-status-dialog").dialog("open");
		}
		return false;
	});

	/*
	 * Details buttons
	 */
	$(".details").each(function(i, e) {
		$(this).click(function() {
			$(".details-dialog[id="+$(this).attr("id")+"]").dialog("open");
			return false;
		});
	});

	/*
	 * Change content buttons
	 */
	$(".change-content").each(function() {
		$(this).click(function() {
			$("#change-content-form").resetForm();
			$("#change-content-form #error-show").hide();
			$("#change-content-dialog #new-content-label").html("New " + $(this).attr("content"));
			$("#change-content-dialog input:submit").attr("value", "Change " + $(this).attr("content"));
			switch ($(this).attr("content")) {
				case "username":
					$("#change-content-dialog input:text").attr("class", "required lettersdigits");
					break;
				case "email":
					$("#change-content-dialog input:text").attr("class", "required email");
					break;
				case "phone number":
					$("#change-content-dialog input:text").attr("class", "required digits");
					break;
				default:
					$("#change-content-dialog input:text").attr("class", "required");
					break;
			}
			$("#change-content-dialog")
				.attr("content", $(this).attr("content"))
				.attr("for", $(this).attr("id"))
				.dialog({title: "Change user's " + $(this).attr("content")})
				.dialog("open");
			return false;
		});
	});

	/*
	 * Change password buttons
	 */
	 $(".change-password").each(function(i, e) {
	 	$(this).click(function() {
	 		$("#change-password-form").resetForm();
	 		$("#change-password-form #error-show").hide();
	 		$("#change-password-dialog").attr("for", $(this).attr("id")).dialog("open");
	 		return false;
	 	});
	 });

	/*
	 * Sort buttons
	 */
	// $("button.sort").button({
	// 	icons: {
	// 		primary: "ui-icon-triangle-1-s"
	// 	},
	// 	text: false
	// });

	/*
	 * Init dialogs
	 */
	$(".dialog table, .dialog tr, .dialog td").addClass("noborder");
	function formValidate(element) {
		return $(element).validate({
			errorClass: "text-error",
			validClass: "text-success",
			errorElement: "span",
			errorPlacement: function(error, element) {
				$("[id=error-show]").html(error);
			}
		}).form();
	}

	/*
	 * Change content dialogs
	 */
	$("#change-content-form").submit(function() {
		$("#change-content-form #error-show").show();
		$(this).ajaxSubmit({
			data: {type: "change-content", content: $("#change-content-dialog").attr("content"), id: $("#change-content-dialog").attr("for")},
			beforeSubmit: function() {
				return formValidate("#change-content-form");
			},
			success: function(data) {
				if (data == "") {
					$(".change-content[id=" + $("#change-content-dialog").attr("for") + "][content=" + $("#change-content-dialog").attr("content") + "]")
						.text($("#change-content-form #id_new_content").val());
					$("#change-content-dialog").dialog("close");
					$("#notice-dialog").html("User's " + $("#change-content-dialog").attr("content") + "has been updated").dialog("open");
				}
				else
					$("#change-content-form #error-show").html(data);
			}
		});
		return false;
	});

	/*
	 * Change password dialogs
	 */
	$("#change-password-dialog input:password").addClass("required");
	$("#change-password-dialog #id_new_pass").attr("minlength", "6");
	$("#change-password-dialog #id_confirm_pass").attr("equalTo", "#id_new_pass");
	$("#change-password-form").submit(function() {
		$("#change-password-form #error-show").show();
		$(this).ajaxSubmit({
			data: {type: "change-password", id: $("#change-password-dialog").attr("for")},
			beforeSubmit: function() {
				return formValidate("#change-password-form");
			},
			success: function(data) {
				if (data == "") {
					$("#change-password-dialog").dialog("close");
					$("#notice-dialog").html("User's password has been updated").dialog("open");
				}
				else
					$("#change-password-form #error-show").html(data);
			}
		});
		return false;
	});

	/*
	* Set status dialog
	*/
	$("#set-status-dialog").dialog({
		buttons: {
			"Yes": function() {
				$.ajax({
					type: "POST",
					url: "/admin/",
					data: {type: "set-status", id: $(this).attr("set-status-for")},
					success: function(data) {
						$("#set-status-dialog").dialog("close");
						$("a.set-status[id="+$("#set-status-dialog").attr("set-status-for")+"]")
							.attr("mode", $("#set-status-dialog").attr("mode")=="True"?"False":"True")
							.text($("#set-status-dialog").attr("mode")=="True"?"Activate":"Deactivate");
					}
				});
			},
			"No": function() {
				$(this).dialog("close");
			}
		}
	});

	/*
	 * Set multi status dialog
	 */
	$("#set-multi-status-dialog #radio").buttonset();
	$("#set-multi-status-dialog").dialog({
		buttons: {
			"Yes": function() {
				$("input.check:checked").each(function(i, e) {
					$(this).attr("name", "for").attr("value", $(this).attr("id"));
				});
				var post_data = [{name: "type", value: "set-multi-status"}];
				post_data.push({name: "mode", value: $("#set-multi-status-dialog input:checked").attr("id")});
				post_data = post_data.concat($("input.check:checked").serializeArray());
				$.ajax({
					type: "POST",
					url: "/admin/",
					data: post_data,
					dataType: "json",
					success: function(data) {
						$("input.check:checked").each(function(i, e) {
							$(".set-status[id=" + $(this).attr("id") + "]")
								.text(post_data[1].value == "activate" ? "Deactivate" : "Activate");
						});
						$("#set-multi-status-dialog").dialog("close");
						$("#notice-dialog").html(data ? data : "Users' status have been updated").dialog("open");
					}
				});
			},
			"No": function() {
				$(this).dialog("close");
			}
		}
	});
});