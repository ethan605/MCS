$(document).ready(function() {
	$(".link").removeClass("link").addClass("ui-state-default ui-corner-all ui-button ui-button-link");
	$("input:submit, a.button, button").button();
	$("#content, #footer").hide();
	$("#header").hide().slideDown(function() {
		$("#content").fadeIn(function() {
			$("#footer").slideDown();
		});
	});
	$(".dialog").dialog({
		autoOpen: false,
		modal: true,
		resizable: false,
		show: "blind",
		hide: "blind",
	});
	$("#notice-dialog").dialog({
		buttons: {
			"OK": function() {
				$(this).dialog("close");
			}
		}
	})
	$("#confirm-dialog").dialog({
		buttons: {
			"Yes": function() {
				$(this).dialog("close");
			},
			"No": function() {
				$(this).dialog("close");
			}
		}
	})
});