$(document).ready(function() {
	// first time load recent site
	makeRecentSiteAjaxCall();
	$('#loader').fadeOut('slow', function() {
		$(this).css("display","none");
	});
	$('#table-container').fadeIn('slow', function() {
		$(this).css("display","");
	});
	
	$("#allSiteButton").click(function() {
		$("#table-container").css("display", "none");
		$("#loader").css("display", "");
		makeAllSiteAjaxCall()
		$('#loader').fadeOut('slow', function() {
			$(this).css("display","none");
		});
		$('#table-container').fadeIn('slow', function() {
			$(this).css("display","");
		});
	});

	$("#recentSiteButton").click(function() {
		$("#table-container").css("display", "none");
		$("#loader").css("display", "");
		makeRecentSiteAjaxCall()
		$('#loader').fadeOut('slow', function() {
			$(this).css("display","none");
		});
		$('#table-container').fadeIn('slow', function() {
			$(this).css("display","");
		});
	});
	
	/*
	 * Table Events Handler
	 */
	// reset table
	$("body").on("click", "#resetButton", function() { 
		resetTable();
	});
	
	// filter for country
	$("body").on("change", "#countryButtonGroup input[type='radio']", function() {
		switch($(this).val()) {
		case 'All Country':
			table.search('').column(5).search('').draw();
			break;
		default:
			table.search('').column(5).search($(this).val()).draw();
		break;
		}
	});
	
	// filter for country dropdown in mobile
	$("body").on("change", "#countryDropList", function(){
		switch($(this).val()) {
		case 'All Solution':
			table.search('').column(5).search('').draw();
			break;
		default:
			table.search('').column(5).search($(this).val()).draw();
		break;
		}
	});
	
	// filter for category
	$("body").on("change", "#categoryList", function(){
		switch($(this).val()) {
		case 'All Category':
			table.search('').column(6).search('').draw();
			break;
		default:
			table.search('').column(6).search($(this).val()).draw();
		break;
		}
	});
	
	// filter for select
	$("body").on("change", "#solutionList", function(){
		switch($(this).val()) {
		case 'All Solution':
			table.search('').column(7).search('').draw();
			break;
		default:
			table.search('').column(7).search($(this).val()).draw();
		break;
		}
	});
	
	
	/*
	 * Update recent site handler 
	 */
	$("body").on("click", ".site-anchor", function(){
		var id = $(this).parent().siblings(":first").text();
		updateRecentSiteAjax(id);
	});
	
});// $( document ).ready(function()
function getMediaType() {
	if (window.matchMedia("(min-width: 1651px)").matches) {
		return "monitor";
	}else if (window.matchMedia("(min-width: 1650px)").matches) {
		return "laptop";
	} else if (window.matchMedia("(min-width: 992px)").matches) {
		return "desktop";
	} else if (window.matchMedia("(min-width: 768px)").matches) {
		return "tablet";
	} else if (window.matchMedia("(min-width: 544px)").matches) {
		return "phablet";
	} else if (window.matchMedia("(min-width: 320px)").matches) {
		return "phone";
	} else {
		return "tiny";
	}
}

function showTable(data) {
	//console.log("table data : " + data)
	$("#table-container").empty();
	$("#table-container").append(data);
}

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function makeAllSiteAjaxCall() {
	/*
	 * // not needed as we are doing only get request var csrftoken =
	 * Cookies.get('csrftoken');
	 * 
	 * $.ajaxSetup({ beforeSend: function(xhr, settings) { if
	 * (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	 * xhr.setRequestHeader("X-CSRFToken", csrftoken); } } });
	 */

	var jqxhr = $.get({
		url : "/QuickLink/home/allsite",
		cache:false
	}, function(data) {
		showTable(data);
		bindAndReset();
	}).done(function() {
		// console.log("second success");
	}).fail(function() {
		console.log("error while call allsite");
	}).always(function() {
		//console.log("all site ajax finished");
	});
}

function makeRecentSiteAjaxCall() {
	/*
	 * // not needed as we are doing only get request var csrftoken =
	 * Cookies.get('csrftoken');
	 * 
	 * $.ajaxSetup({ beforeSend: function(xhr, settings) { if
	 * (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	 * xhr.setRequestHeader("X-CSRFToken", csrftoken); } } });
	 * 
	 */
	rowcount = 10
	var mediaType = getMediaType();
	switch (mediaType) {
	case 'monitor':
		rowcount = 15;
		break;
	case 'laptop':
		rowcount = 10;
		break;
	case 'desktop':
		rowcount = 10;
		break;
	case 'tablet':
		rowcount = 10;
		break;
	case 'phablet':
		rowcount = 10;
		break;
	case 'phone':
		rowcount = 10;
		break;
	case 'tiny':
		break;
	default:
		console.log("unknown device type");
	}
	var jqxhr = $.get({
		url : "/QuickLink/home/recentsite",
		cache : false
	},
	{
		rowcount: rowcount
	}, function(data) {
		showTable(data);
		bindAndReset();
	}).done(function() {
		// console.log("second success");
	}).fail(function() {
		console.log("error while calling recentsite");
	}).always(function() {
		//console.log("recent site ajax finished");
	});
}

function bindAndReset() {
	bindTable();
	resetTable();
}

function resetTable() {
	// reset table
	table.search('').columns().search('').draw();
	$("#labelCountryALL").button('toggle'); //for desktop
	$("#countryDropList")[0].selectedIndex = 0; //for mobile
	$("#solutionList")[0].selectedIndex = 0; 
	$("#categoryList")[0].selectedIndex = 0;
}
// this function must be called when at last, when table is populated completely
function bindTable() {
	lengthmenu = [ [ 10, 25, 50, -1 ], [ 10, 25, 50, "All" ] ]
	var mediaType = getMediaType();
	switch (mediaType) {
	case 'monitor':
		lengthmenu = [[15, 25, 50, -1], [15, 25, 50, "All"]];
		break;
	case 'laptop':
		lengthmenu = [[10, 25, 50, -1], [10, 25, 50, "All"]];
		break;
	case 'desktop':
		lengthmenu = [[10, 25, 50, -1], [10, 25, 50, "All"]];
		break;
	case 'tablet':
		lengthmenu = [[10, 25, 50, -1], [10, 25, 50, "All"]];
		break;
	case 'phablet':
		lengthmenu = [[10, 25, 50, -1], [10, 25, 50, "All"]];
		break;
	case 'phone':
		lengthmenu = [[10, 10, 25, -1], [10, 10, 25, "All"]];
		break;
	case 'tiny':
		break;
	default:
		console.log("unknown device type");
	}
	table = $('#urltable').DataTable({
		// table options
		"deferRender" : true,
		"lengthMenu" : lengthmenu,
		"columnDefs" : [ {
			"orderable" : false,
			targets : [ 2, 3, 4 ]
		}, {
			"searchable" : false,
			targets : [ 2, 3, 4 ]
		} ],
	    "order": [] //disable default ordering, default ordering is done on server
	});
	// set focus on search box
	$("input[type='search']").focus();
}

function updateRecentSiteAjax(id) {
	//console.log('updating for site id : ' + id);
	/*
	 * // not needed as we are doing only get request var csrftoken =
	 * Cookies.get('csrftoken');
	 * 
	 * $.ajaxSetup({ beforeSend: function(xhr, settings) { if
	 * (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	 * xhr.setRequestHeader("X-CSRFToken", csrftoken); } } });
	 * 
	 */
	var jqxhr = $.get({
		url : "/QuickLink/home/updaterecent"
	}, 
	{
		siteid: id
	},function(data) {
		// console.log(data.rc + " : " + data.rt);
	}).done(function() {
		// console.log("second success");
	}).fail(function() {
		console.log("error while calling recentsite");
	}).always(function() {
		//console.log("recent site ajax finished");
	});
}