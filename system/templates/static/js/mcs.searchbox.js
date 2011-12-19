$(document).ready(function(){
	var searchBox = $("input#searchBox");
	var searchDiv = $("div#searchDiv");
	var searchForm = $("form#searchForm");
	var width = 200;
	var outerWidth = 240;
	var submit = $("#searchSubmit");
	var searchMask = searchBox.val();

	searchForm.submit(function() {
		searchForm.ajaxSubmit({
			success: function(data) {
				if (data != "")
					alert(data);
			}
		});
		return false;
	});
	
	searchBox.bind("focus", function() {
		if(searchBox.val() === searchMask)
			searchBox.val("");
		$(this).animate({color: "#000"}, 300); // text color
		$(this).parent().animate({
			width: outerWidth + "px",
			backgroundColor: "#fff", // background color
			paddingRight: "43px"
		}, 300, function() {
			if(!(searchBox.val() === "" || searchBox.val() === searchMask))
				if(!($.browser.msie && $.browser.version < 9))
					submit.fadeIn(300);
				else
					submit.css({display: "block"});
		}).addClass("focus");
	}).bind("blur", function() {
		$(this).animate({color: "#b4bdc4"}, 300); // text color
		$(this).parent().animate({
			width: width + "px",
			backgroundColor: "#e8edf1", // background color
			paddingRight: "15px"
		}, 300, function() {
			if(searchBox.val() === "")
				searchBox.val(searchMask)
		}).removeClass("focus");
		if(!($.browser.msie && $.browser.version < 9))
			submit.fadeOut(100);
		else
			submit.css({display: "none"});
	});
});