$(document).ready(function() {
	bindTable();
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
			table.search('').column(3).search('').draw();
			break;
		default:
			table.search('').column(3).search($(this).val()).draw();
		break;
		}
	});
	
	// filter for country dropdown in mobile
	$("body").on("change", "#countryDropList", function(){
		switch($(this).val()) {
		case 'All Solution':
			table.search('').column(3).search('').draw();
			break;
		default:
			table.search('').column(3).search($(this).val()).draw();
		break;
		}
	});
	
	// filter for category
	$("body").on("change", "#categoryList", function(){
		switch($(this).val()) {
		case 'All Category':
			table.search('').column(4).search('').draw();
			break;
		default:
			table.search('').column(4).search($(this).val()).draw();
		break;
		}
	});
	
	// filter for select
	$("body").on("change", "#solutionList", function(){
		switch($(this).val()) {
		case 'All Solution':
			table.search('').column(5).search('').draw();
			break;
		default:
			table.search('').column(5).search($(this).val()).draw();
		break;
		}
	});
	
});// $( document ).ready(function()


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
	table = $('#urltable').DataTable({
		// table options
		"deferRender" : true,
		"lengthMenu" : [ [ 10, 25, 50, -1 ], [ 10, 25, 50, "All" ] ],
		"columnDefs" : [ {
			"orderable" : false,
			targets : [ 0, 1]
		}, {
			"searchable" : false,
			targets : [ 0, 1 ]
		} ],
	    "order": [] //disable default ordering, ordering is done on server
	});

	// make page visible
	$('#loader').fadeOut('slow', function() {
		$(this).css("display","none");
	});
	$('#table-container').fadeIn('slow', function() {
		$(this).css("display","");
	});
	$("input[type='search']").focus();
}