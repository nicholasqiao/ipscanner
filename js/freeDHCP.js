(function () {
	$(document).ready(function() {
		$("#listDHCP").click(function () {
			console.log("hit");
			var ipaddress = document.getElementById('ipaddress').value;
			var location = "---";
			var hostname = "";
			var type = "DHCP";
			var state = document.getElementById('state').value;
		
			$.ajax({
				type: "POST", 
				url: "php/generateTable.php", 
				data: ({ipaddress: ipaddress, location: location, hostname: hostname, type: type, state: state}), 
				success: function (data) {
					
    				$("#addresstable").remove();
					
					$("#tablehere").html(data);
					$("#addresstable").tablesorter();
					
					var itemCount = document.getElementById("addresstable").rows.length - 1;
					$("#itemCount").html("Item count: " + itemCount);

					var table = document.getElementById("addresstable");
					var staticFree = 0;
					var dhcpFree = 0;

					for (x = 1; x < itemCount+1; x++) {
						if (table.rows[x].cells[1].firstChild.data == "---") {
							if (table.rows[x].cells[3].firstChild.data == "DHCP") {
								dhcpFree++;
							} else {
								staticFree++;
							}
						}
					}
					
					$("#staticCount").html("Free Static: ");
					document.getElementById("listStatic").style.display = "block";

					$("#dhcpCount").html("Free DHCP: ");
					document.getElementById("listDHCP").style.display = "block";

					var $table = $('#addresstable');
					$table.floatThead();
				}
			});
		});
	});
})();
