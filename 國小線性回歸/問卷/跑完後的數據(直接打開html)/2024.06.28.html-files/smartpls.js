$(document).ready(function() {

	$('ul.nav-tabs li a').click(function (e) {
	  e.preventDefault()
	  $(this).tab('show')
	});

});