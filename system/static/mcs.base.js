$(document).ready(function() {
	$(".link").removeClass("link").addClass("ui-state-default ui-corner-all ui-button ui-button-link");
	$("input:submit, a.button, button").button();
	$(".dialog").dialog({
		autoOpen: false,
		modal: true,
		resizable: false,
		show: "blind",
		hide: "blind"
	});
	$("#notice-dialog").dialog({
		buttons: {
			"OK": function() { 
				$(this).dialog("close"); 
			}
		}
	});
});