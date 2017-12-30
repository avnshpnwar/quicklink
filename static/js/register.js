$(document).ready(function() {
	console.log("register ready!");
	
	jQuery.validator.addMethod(
		"uidreg", 
		function(value, element) {
			return  /^[a-z]+$/.test(value);
		}, 
		"userid must be smallcase without space"
	);
	
	jQuery.validator.addMethod(
		"pwdreg",
		function(value, element) {
			return /^[^\s]+$/.test(value);
		},
		"password can't contain space"
	);
	$("#register-form").validate({
		rules : {
			uid : {
				uidreg : true,
				minlength: 2
			},
			pwda : {
				pwdreg : true,
			},
			pwdb : {
				equalTo: "#register-form [name=pwda]"
			},
		},
		messages : {
			pwdb : {
				equalTo: 'Password do not match'
			}
		},
		tooltip_options: {
	        uid : { placement: 'top' },
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
