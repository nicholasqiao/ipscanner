<?php

	$ipaddress = $_POST['ipaddress'];
	$location = $_POST['location'];
	$hostname = $_POST['hostname'];
	$type = $_POST['type'];
	$state = $_POST['state'];

	$mysqli = new mysqli("", "", "", "");
	if ($mysqli->connect_errno) {
	    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
	}

	$query = "";
	if ($ipaddress == "" and $location == "" and $hostname == "" and $type == "" and $state == "") {
		$query = "SELECT * FROM ipaddresslist limit 0";
	} else {
		$query = "SELECT * FROM ipaddresslist WHERE ipaddress LIKE '%{$ipaddress}%' 
		AND location LIKE '%{$location}%' AND hostname LIKE '%{$hostname}%' AND type LIKE '%{$type}%' AND state LIKE '%{$state}%'";
	}
	
	$result = $mysqli->query($query);
	
	echo "<table id='addresstable' class='u-full-width tablesorter'>";

	echo "<thead>";
	echo "<tr>";
	echo "<th>IP Address</th>";
	echo "<th>Location</th>";
	echo "<th>Hostname</th>";
	echo "<th>Static/DHCP</th>";
	echo "<th>Pingable</th>";
	echo "</tr>";
	echo "</thead>";

	echo "<tbody>";

	while ($row = $result->fetch_array()) {
		if ($row['errors'] == "Mismatch") {
			echo "<tr class='temp'>";
	        echo "<td class='temp mismatch'>" . $row['ipaddress'] . "</td>";
	        echo "<td class='temp mismatch'>" . $row['location'] . "</td>";
	        echo "<td class='temp mismatch'>" . $row['hostname'] . "</td>";
	        echo "<td class='temp mismatch'>" . $row['type'] . "</td>";
	        echo "<td class='temp mismatch'>" . $row['state'] . "</td>";
	        echo "</tr>";
		} else {
			echo "<tr class='temp'>";
	        echo "<td class='temp'>" . $row['ipaddress'] . "</td>";
	        echo "<td class='temp'>" . $row['location'] . "</td>";
	        echo "<td class='temp'>" . $row['hostname'] . "</td>";
	        echo "<td class='temp'>" . $row['type'] . "</td>";
	        echo "<td class='temp'>" . $row['state'] . "</td>";
	        echo "</tr>";
		}
	}

	echo "</tbody>";
	echo "</table>";
?>
