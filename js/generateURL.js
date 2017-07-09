(function () {
	$(document).ready(function() {
		$("#generateURL").click(function () {
			var ipaddress = document.getElementById('ipaddress').value;
			var location = document.getElementById('location').value;
			var hostname = document.getElementById('hostname').value;
			var type = document.getElementById('type').value;
			var state = document.getElementById('state').value;

			var generatedURL = "http://127.0.0.1/?ipaddress=" + ipaddress + "&location=" 
			+ location + "&hostname=" + hostname + "&type=" + type + "&state=" + state;
			
			window.prompt("Link Generated: ", generatedURL);
		});
	});
})();
