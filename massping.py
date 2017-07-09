#!/usr/bin/python

import os
import subprocess
import mysql.connector
import time
from datetime import datetime

print "Starting Mass Ping"
active = []
inactive = []

subnets = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4", "127.0.0.5", "127.0.0.6", "127.0.0.7", "127.0.0.8"]

for x in range(0,8,2):
	string = ""
	ping = subprocess.Popen(
	["fping", "-g", subnets[x], subnets[x+1]],
	stdout = subprocess.PIPE,
	stderr = subprocess.PIPE
	)

	out, error = ping.communicate()

	string = out

	for line in string.splitlines():
		if "alive" in line:
			active.append(str(line.split(" ")[0]))
		else:
			inactive.append(str(line.split(" ")[0]))

print "Finished Mass Ping"
print "Attempting To Connect To Database"

db = mysql.connector.connect (
	user='',
	password=,
	host='',
	database=''
)

if db:
	print "Connection Successful!"

pingdb = mysql.connector.connect (
	user='',
	password=,
	host='',
	database=''
)

if pingdb:
	print "Connection to PING DATABASE Successful!"

cursor = db.cursor();
table = 'IP'

activeInfo = []
inactiveInfo = []

for x in active:
	if x is not "":
		targetIP = "'" + x + "'"

		cursor.execute (
			"SELECT Sheet1.location, IP.IP_addr, Sheet1.Hostname "
			"FROM Sheet1, IP "
			"WHERE Sheet1.ID = IP.ID "
			"AND IP.IP_addr = " + targetIP
		)

		row = cursor.fetchall()

		#This is if IP is not in BOTL
		if len(row) is not 0:
			activeInfo.append([str(row[0][0]), str(row[0][1]), str(row[0][2])])	
		else:
			activeInfo.append([str("---"), x, str("---")]);	

for x in inactive:
	targetIP = "'" + x + "'"

	cursor.execute (
		"SELECT Sheet1.location, IP.IP_addr, Sheet1.Hostname "
		"FROM Sheet1, IP "
		"WHERE Sheet1.ID = IP.ID "
		"AND IP.IP_addr = " + targetIP
	)
	row = cursor.fetchall()

	if len(row) is not 0:
		inactiveInfo.append([str(row[0][0]), str(row[0][1]), str(row[0][2])])	
	else:
		inactiveInfo.append([str("---"), x, str("---")]);	

wipecursor = pingdb.cursor()
wipecursor.execute(
	"TRUNCATE TABLE ipaddresslist"
)

for x in activeInfo:
	location = x[0]
	ipaddress = x[1]
	hostname = x[2]

	if (len(ipaddress) == 12 and int(ipaddress[-3:]) > 239):
		IPtype = "DHCP"
	else:
		IPtype = "Static";

	pingcursor = pingdb.cursor()
	add_address = (
		"INSERT INTO ipaddresslist "
		"(ipaddress, location, hostname, type, state, errors) "
		"VALUES (%s, %s, %s, %s, %s, %s)"
	)

	#Check for hostname errors
	checkHost = subprocess.Popen(
		["host", ipaddress],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
	)

	out, error = checkHost.communicate()
	lastValue = out.split(' ')
	campusHostName = lastValue[-1][:-22]

	if (len(location) == 0 or location == ""):
		location = "---"

	# if (campusHostName != hostname and hostname != "---"):
	if (campusHostName != hostname):
		if (campusHostName == ""):
			pingcursor.execute(add_address, (ipaddress, location, "---", IPtype, 'Yes', 'Mismatch'))
		else: 
			pingcursor.execute(add_address, (ipaddress, location, campusHostName, IPtype, 'Yes', 'Mismatch'))
		
	else:
		pingcursor.execute(add_address, (ipaddress, location, hostname, IPtype, 'Yes', 'None'))

	pingdb.commit()

for x in inactiveInfo:
	location = x[0]
	ipaddress = x[1]
	hostname = x[2]

	if (len(ipaddress) == 12 and int(ipaddress[-3:]) > 239):
		IPtype = "DHCP"
	else:
		IPtype = "Static";

	pingcursor = pingdb.cursor()
	add_address = (
		"INSERT INTO ipaddresslist "
		"(ipaddress, location, hostname, type, state, errors) "
		"VALUES (%s, %s, %s, %s, %s, %s)"
	)

	#Check for hostname errors
	checkHost = subprocess.Popen(
		["host", ipaddress],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
	)

	out, error = checkHost.communicate()
	lastValue = out.split(' ')
	campusHostName = lastValue[-1][:-22]

	if (len(location) == 0 or location == ""):
		location = "---"

	# if (campusHostName != hostname and hostname != "---"):
	if (campusHostName != hostname):
		if (campusHostName == ""):
			pingcursor.execute(add_address, (ipaddress, location, "---", IPtype, 'No', 'Mismatch'))
		else: 
			pingcursor.execute(add_address, (ipaddress, location, campusHostName, IPtype, 'No', 'Mismatch'))
	
	else:
		pingcursor.execute(add_address, (ipaddress, location, hostname, IPtype, 'No', 'None'))

	pingdb.commit()


	time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	currentTime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").strftime("%I:%M:%S %p %m-%d-%Y ")

	jsfile = open('js/lastmodified.js', 'w')
	jsfile.write("document.getElementById(\"lastModified\").innerHTML = \"Page last updated: " + currentTime + " \";")

	modfile = open('js/lastmod.txt', 'w')
	modfile.write("Page last updated: " + currentTime)















