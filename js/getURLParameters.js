$(document).ready(function() {
	var url = window.location.search.substring(1);
	var postSplit = url.split("&");

	for (x = 0; x < postSplit.length; x++) {
		var array = postSplit[x].split("=");
		var field = array[0];
		var value = array[1];

		document.getElementById(field).value = value;
	}
});
