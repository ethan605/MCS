/*
 * MCS Admin functions
 */
$(document).ready(function() {
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
	$(".change-content").each(function(i, e) {
		$(this).click(function() {
			return false;
		});
	});

	/*
	 * Change password buttons
	 */
	 $(".change-content").each(function(i, e) {
	 	$(this).click(function() {
	 		$("#change-password-dialog").dialog("open");
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
	 * Checkboxes
	 */
	 $("input#check-all").click(function() {
	 	if ($(this).is(":checked"))
	 		$("input.check:not(:checked)").attr("checked", "checked")
	 	else
	 		$("input.check:checked").removeAttr("checked");
	 });

	/*
	 * Init dialogs
	 */
	$(".dialog table, .dialog tr, .dialog td").addClass("noborder");
	$(".details-dialog").dialog({
		autoOpen: false,
		modal: true,
		resizable: false,
		show: "blind",
		hide: "blind",
		buttons: {
			"OK": function() {
				$(this).dialog("close");
			}
		}
	});
	$("#change-password-dialog").dialog({
	});
	$("#set-status-dialog").dialog({
		autoOpen: false,
		modal: true,
		show: "blind",
		hide: "blind",
		resizable: false,
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
});