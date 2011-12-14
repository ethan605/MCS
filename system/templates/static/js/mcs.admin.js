/*
 * MCS Admin functions
 */
$(document).ready(function() {
	$("#tabs").tabs();
	$("#all-user-table tfoot tr").addClass("noborder")
		.children().addClass("noborder");
	/*
	 * Init elements
	 * Buttons
	 */
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
	 * Change single status buttons
	 */
	$(".change-single.status").each(function() {
		$(this).text($(this).attr("mode")=="True" ? "Deactivate":"Activate");
		$(this).click(function() {
			$("#change-single-status-dialog").attr("mode", $(this).attr("mode"))
				.attr("for", $(this).attr("id"))
				.html("Do you really want to " + ($(this).attr("mode")=="True" ? "deactivate":"activate") + " this user?")
				.dialog("open");
			return false;
		});
	});

	/*
	 * Change multi status button
	 */
	$(".change-multi.status").click(function() {
		if ($("input.check:checked").length > 0) {
			$("#change-multi-status-dialog #activate").click();
			$("#change-multi-status-dialog").dialog("open");
		}
		return false;
	});

	/*
	 * Details buttons
	 */
	$(".details").each(function() {
		$(this).click(function() {
			$(".details-dialog[id="+$(this).attr("id")+"]").dialog("open");
			return false;
		});
	});

	/*
	 * Change content buttons
	 */
	$(".change-content").each(function() {
		$(this).attr("display", $(this).attr("content"));
		switch ($(this).attr("content")) {
			case "display-name":
				$(this).attr("display", "display name");
				break;
			case "first-name":
				$(this).attr("display", "first name");
				break;
			case "last-name":
				$(this).attr("display", "last name");
				break;
			case "phone-number":
				$(this).attr("display", "phone number");
				break;
		}
		$(this).click(function() {
			$("#change-content-form").resetForm();
			$("#change-content-form #error-display").hide();
			$("#change-content-form #new-content-label").html("New " + $(this).attr("display"));
			$("#change-content-form input:submit").attr("value", "Change " + $(this).attr("display"));
			switch ($(this).attr("content")) {
				case "username":
					$("#change-content-dialog input:text").attr("class", "required lettersdigits");
					break;
				case "email":
					$("#change-content-dialog input:text").attr("class", "required email");
					break;
				case "phone-number":
					$("#change-content-dialog input:text").attr("class", "required digits");
					break;
				default:
					$("#change-content-dialog input:text").attr("class", "required");
					break;
			}
			$("#change-content-dialog")
				.attr("content", $(this).attr("content"))
				.attr("display", $(this).attr("display"))
				.attr("for", $(this).attr("id"))
				.dialog({title: "Change user's " + $(this).attr("display")})
				.dialog("open");
			return false;
		});
	});

	/*
	 * Change password buttons
	 */
	$(".change-single.password").each(function() {
		$(this).click(function() {
			$("#change-password-form .admin-password").hide();
			$("#change-password-form .admin-password :password").removeClass("required");
			$("#change-password-form").attr("class", "single").resetForm();
			$("#change-password-form #error-display").hide();
			$("#change-password-dialog")
				.attr("for", $(this).attr("id"))
				.dialog({title: "Change user's password"})
				.dialog("open");
			return false;
		});
	});

	$(".change-multi.password").click(function() {
		if ($("input.check:checked").length > 0) {
			$("#change-password-form .admin-password").show();
			$("#change-password-form .admin-password :password").addClass("required");
			$("#change-password-form").attr("class", "multi").resetForm();
			$("#change-password-form #error-display").hide();
			$("#change-password-dialog")
				.dialog({title: "Change multiple passwords"})
				.dialog("open");
		}
		return false;
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
			focusCleanup: true,
			errorClass: "text-error",
			validClass: "text-success",
			errorElement: "span",
			errorPlacement: function(error, element) {
				$("[id=error-display]").html(error);
			}
		}).form();
	}

	/*
	 * Change content dialogs
	 */
	$("#change-content-form").submit(function() {
		$("#change-content-form #error-display").show();
		$(this).ajaxSubmit({
			data: {type: "change content", content: $("#change-content-dialog").attr("content"), id: $("#change-content-dialog").attr("for")},
			beforeSubmit: function() {
				return formValidate("#change-content-form");
			},
			success: function(data) {
				if (data == "") {
					$(".change-content[id=" + $("#change-content-dialog").attr("for") + "][content=" + $("#change-content-dialog").attr("content") + "]")
						.text($("#change-content-form #id_new_content").val());
					$("#change-content-dialog").dialog("close");
					$("#notice-dialog").html("User's " + $("#change-content-dialog").attr("display") + " has been updated").dialog("open");
				}
				else
					$("#change-content-form #error-display").html(data);
			}
		});
		return false;
	});

	/*
	 * Change password dialogs
	 */
	$("#change-password-form #id_new_pass,#id_confirm_pass").addClass("required").attr("minlength", "6");
	$("#change-password-form #id_confirm_pass").attr("equalTo", "#id_new_pass");
	$("#change-password-form").submit(function() {
		$("#change-password-form #error-display").show();
		if ($(this).hasClass("single"))
			$(this).ajaxSubmit({
				data: {type: "single password", id: $("#change-password-dialog").attr("for")},
				beforeSubmit: function() {
					return formValidate("#change-password-form");
				},
				success: function(data) {
					if (data == "") {
						$("#change-password-dialog").dialog("close");
						$("#notice-dialog").html("User's password has been updated").dialog("open");
					}
					else
						$("#change-password-form #error-display").html(data);
				}
			});
		else {
			$("input.check:checked").each(function(i, e) {
				$(this).attr("name", "for").attr("value", $(this).attr("id"));
			});
			var post_data = [{name: "type", value: "multi password"}];
			post_data = post_data.concat($("input.check:checked").serializeArray());
			$(this).ajaxSubmit({
				data: post_data,
				beforeSubmit: function() {
					return formValidate("#change-password-form");
				},
				success: function(data) {
					if (data == "") {
						$(".check, #check-all").removeAttr("checked");
						$("#change-password-dialog").dialog("close");
						$("#notice-dialog").html("Selected users' passwords has been updated").dialog("open");
					}
					else
						$("#change-password-form #error-display").html(data);
				}
			});
		}
		return false;
	});

	/*
	* Set status dialog
	*/
	$("#change-single-status-dialog").dialog({
		buttons: {
			"Yes": function() {
				$.ajax({
					type: "POST",
					url: "/admin/",
					data: {type: "single status", id: $(this).attr("for")},
					success: function(data) {
						$("#change-single-status-dialog").dialog("close");
						$("a.change-single.status[id="+$("#change-single-status-dialog").attr("for")+"]")
							.attr("mode", $("#change-single-status-dialog").attr("mode")=="True"?"False":"True")
							.text($("#change-single-status-dialog").attr("mode")=="True"?"Activate":"Deactivate");
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
	$("#change-multi-status-dialog #radio").buttonset();
	$("#change-multi-status-dialog").dialog({
		buttons: {
			"Yes": function() {
				$("input.check:checked").each(function(i, e) {
					$(this).attr("name", "for").attr("value", $(this).attr("id"));
				});
				var post_data = [{name: "type", value: "multi status"}];
				post_data.push({name: "mode", value: $("#change-multi-status-dialog input:checked").attr("id")});
				post_data = post_data.concat($("input.check:checked").serializeArray());
				$.ajax({
					type: "POST",
					url: "/admin/",
					data: post_data,
					dataType: "json",
					success: function(data) {
						$("input.check:checked").each(function(i, e) {
							$(".change-single.status[id=" + $(this).attr("id") + "]")
								.attr("mode", post_data[1].value == "activate" ? "True" : "False")
								.text(post_data[1].value == "activate" ? "Deactivate" : "Activate");
						})
						$(".check, #check-all").removeAttr("checked");
						$("#change-multi-status-dialog").dialog("close");
						$("#notice-dialog").html(data ? data : "Selected users' statuses have been updated").dialog("open");
					}
				});
			},
			"No": function() {
				$(this).dialog("close");
			}
		}
	});
});