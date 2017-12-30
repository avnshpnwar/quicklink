$(document).ready(function() {
	console.log("changepwd ready!");
	
	jQuery.validator.addMethod(
		"pwdreg",
		function(value, element) {
			return /^[^\s]+$/.test(value);
		},
		"password can't contain space"
	);
	
	$("#changepwd-form").validate({
		rules : {
			cpwd : {
				pwdreg : true
			},
			pwda : {
				pwdreg : true
			},
			pwdb : {
				equalTo: "#changepwd-form [name=pwda]"
			},
		},
		messages : {
			pwdb : {
				equalTo: 'Password do not match'
			}
		},
		tooltip_options: {
	        cpwd : { placement: 'top' },
	        pwda : {placement: 'top'},
	        pwdb :{ placement : 'top'} 
	    },
		// Make sure the form is submitted to the destination defined
		// in the "action" attribute of the form when valid
		submitHandler : function(form) {
			form.submit();
		}
	});

});// $( document ).ready(function()
