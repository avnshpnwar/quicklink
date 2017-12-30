$(document).ready(function() {
	console.log("logon ready!");

	$("#login-form").validate({
		tooltip_options: {
	        uid : { placement: 'top' },
	        pwd : {placement: 'top'}
	    },
		// Make sure the form is submitted to the destination defined
		// in the "action" attribute of the form when valid
		submitHandler : function(form) {
			form.submit();
		}
	});

});// $( document ).ready(function()
