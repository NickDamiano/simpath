from modules import calculate_position as position
from flask import Flask, redirect, url_for, render_template, request, session, jsonify, Response
import pdb
import pickle
import time
import json
import pandas as pd
import numpy as np 

app = Flask(__name__)

# Sets the start time for a specific aircraft to current time in epoch and writes it back to the file
@app.route('/start', methods=['POST'])
def start_flying():
	start_time = ""

	# identify the aircraft name from keys passed
	aircraft_names	= request.get_json()
	# Convert existing aircraft to python object
	vessels_dict = convert_aircraft_to_python_object()

	# find the vessel name we are starting, set current time (time since epoch)
	for aircraft_name in aircraft_names["aircraft_names"]:
		for vessel in vessels_dict:
			if(vessel["name"] == aircraft_name):
				start_time = time.time()
				vessel["start_time"] = start_time

	# Write the updated aircraft data back to file and return the name and start time as json object
	write_aircraft(vessels_dict)
	return jsonify({"aircraft_name": aircraft_name, "start_time": start_time})

# Sets the start time for a specific aircraft to current time in epoch and writes it back to the file
@app.route('/stop', methods=['POST'])
def stop_flying():

	# identify the aircraft name from keys passed
	aircraft_names	= request.get_json()
	# Convert existing aircraft to python object
	vessels_dict = convert_aircraft_to_python_object()

	# find the vessel name we are starting, set current time (time since epoch)
	for aircraft_name in aircraft_names["aircraft_names"]:
		for vessel in vessels_dict:
			if(vessel["name"] == aircraft_name):
				start_time = None
				vessel["start_time"] = start_time

	# Write the updated aircraft data back to file and return the name and start time as json object
	write_aircraft(vessels_dict)
	return jsonify({"aircraft_name": aircraft_name, "start_time": start_time})

@app.route('/startAll', methods=["POST"])
def start_flying_all():
	start_time = ""

	# Convert existing aircraft to python object
	vessels_dict = convert_aircraft_to_python_object()

	# find the vessel name we are starting, set current time (time since epoch)
	for vessel in vessels_dict:
		start_time = time.time()
		vessel["start_time"] = start_time

	# Write the updated aircraft data back to file and return the name and start time as json object
	write_aircraft(vessels_dict)
	return jsonify(vessels_dict)

# Takes a json file with 1 or more aircraft, pulls the existing planes, appends the new planes to it and saves it. 
@app.route('/CreateAircraft', methods=['POST'])
def create_aircraft():
	# Load pickle data of existing aircraft and convert to python dict/object
	all_aircraft = convert_aircraft_to_python_object()
	# if the file was empty, pass an empty array
	if not all_aircraft:
		all_aircraft = []

	# parse the json file passed in
	new_aircraft = request.get_json()

	# Check for single points to translate into an array of orbit points

	# Iterate through the new aircraft and append them to the existing aircraft
	for aircraft in new_aircraft:
		all_aircraft.append(aircraft)

	# write all aircraft back to database/bytes file
	write_aircraft(all_aircraft)

	# Convert the aircraft into json and return it along with 201 status as JSON
	json_all_aircraft = json.dumps(all_aircraft)
	return Response(json_all_aircraft, status=201, mimetype='application/json')

# Returns all aircraft positions in json object. 
@app.route('/AllAircraftPositions', methods=["GET"])
def get_all_positions():
	# Set Initial variable data to base value
	distance_traveled = 0
	current_bearing = ""
	aircraft_results = []

	# Convert existing aircraft data to json object
	all_aircraft = convert_aircraft_to_python_object()

	# Iterate through 
	for aircraft in all_aircraft:
		waypoints = aircraft["waypoints"]
		# current time minus start time * 0.514444 (knots to meters per second) times the speed of the aircraft
		# 	= distance traveled converted to integer
		if aircraft["start_time"] != None:	
			# Calculate distance traveled
			distance_traveled = int((time.time() - aircraft["start_time"]) * (aircraft["cruising_speed"] * .514444))
			print("distance traveled")

			# pass the waypoints and distance to helper function, which figures out the start point
			# 	and returns the bearing of travel, point to measure from, and distance from that point
			start_index, current_bearing, relative_distance_traveled = calculate_segment_start_and_bearing(waypoints, distance_traveled)
			start_point = waypoints[start_index]
			start_lat 	= start_point.split(",")[0]
			start_long	= start_point.split(",")[1]

			new_long, new_lat = position.calculate(start_lat, start_long, 
				relative_distance_traveled / 1000,current_bearing)
			result = {"name": aircraft["name"], "altitude": aircraft["altitude"], "new_lat": new_lat, "new_long": new_long }
			aircraft_results.append(result)
	return jsonify(aircraft_results)

# returns calculation of new position with explicitly passed in paramters
@app.route('/calculate_coords', methods=['GET'])
def set_aircraft_data():
	latitude 	= float(request.args.get('latitude'))
	longitude 	= float(request.args.get('longitude'))
	distance	= float(request.args.get('distance'))
	bearing		= float(request.args.get('bearing'))

	new_lat, new_long = position.calculate(latitude,longitude,distance,bearing)
	return jsonify({'latitude': new_lat, 'longitude': new_long })

# Returns all aircraft json object which contains data about the aircraft but not present position
@app.route('/GetAllAircraft', methods=['GET'])
def print_all_aircraft():
	# open the file to read, load the file to be a python object
	file = open('aircraft', 'rb')
	vessels = pickle.load(file)
	
	# find the vessel name we are starting, set current time (time since epoch)
	return jsonify(vessels)

########################################## helper methods ##########################################


# calculates the distance from 1st,2nd,3rd...last,1st. after last - aircraft
# 	will return to start and continue the track. so it figures out that full 
# 	loop distance in miles and returns it.
def calculate_roundtrip_distance(waypoints):
	total_distance = 0
	# for waypoint in waypoints:
	# We measure from index to index+1 so we want to stop before out of index error
	# this measures the segment distance
	for index, waypoint in enumerate(waypoints):
		if index != len(waypoints) -1:
			split_start = waypoint.split(",")
			split_end = waypoints[index+1].split(",")
			lat1 = split_start[0]
			lon1 = split_start[1]
			lat2 = split_end[0]
			lon2 = split_end[1]
			segment_distance = position.calculate_distance(lat1,lon1,lat2,lon2)
			total_distance += segment_distance
	# Finally add the segment from end to start since we're looping these tracks
	split_start = waypoints[-1].split(",")
	split_end = waypoints[0].split(",")
	lat1 = split_start[0]
	lon1 = split_start[1]
	lat2 = split_end[0]
	lon2 = split_end[1]
	total_distance += position.calculate_distance(lat1,lon1,lat2,lon2)
	total_distance

	return total_distance

# Takes an array of waypoints, a distance traveled, and calculates which segments the aircraft would be on
# then returns the latlong for last waypoint completed, bearing from that origin point, and distance forward
def calculate_segment_start_and_bearing(waypoints, distance_so_far):
	start_lat = start_long = end_lat = end_long = segment_bearing = segment_projection_distance= 0
	# rebuild the array with latlong only (convert city state)
	# converted waypoints are array of strings of latlong separated by comma "33.1234,-98.1234"
	converted_waypoints = convert_city_to_coords(waypoints)

	# calculate roundtrip total distance loop
	roundtrip_distance = calculate_roundtrip_distance(converted_waypoints)

	# calculate relative distance in loop (100 mile loop, 103 miles traveled, 3 miles relative)
	relative_distance_so_far = distance_so_far % roundtrip_distance

	# calculate which of the waypoints is the start point (to use to see where along the segment
	# the orbit/track the aircraft is)
	total_distance_calculated 	= 0 
	# index of segment we're checking from
	segment_start 		= 0
	while(total_distance_calculated < relative_distance_so_far):
		# this if block checks if we've now iterated and are on the last waypoint. If so
		#	We set the endpoint to the first index so we can loop back there, otherwise, 
		#   segment end is next waypoint in the list of waypoints
		if segment_start != len(converted_waypoints)-1:
			segment_end = segment_start + 1
		else:
			segment_end = 0
		
		start_lat 		= converted_waypoints[segment_start].split(",")[0]
		start_long 		= converted_waypoints[segment_start].split(",")[1]
		end_lat			= converted_waypoints[segment_end].split(",")[0]
		end_long 		= converted_waypoints[segment_end].split(",")[1]		

		segment_distance = position.calculate_distance(start_lat,start_long,end_lat,end_long)
		up_to_this_segment_distance = total_distance_calculated
		total_distance_calculated += segment_distance

		segment_bearing = position.calculate_bearing(start_lat, start_long, end_lat, end_long) 
		segment_projection_distance = relative_distance_so_far - up_to_this_segment_distance


		# if the accumulated distances of waypoint/segment lengths is still less than the 
		# 	total traveled by the aircraft (within the relative track distance), we increment
		#	segment start to check the next segment length to see if the aircraft falls on that
		#	segment
		if(total_distance_calculated < relative_distance_so_far):
			segment_start += 1

	return segment_start, segment_bearing, segment_projection_distance

# Takes a list of waypoints either in lat long separated by comma or
# city, state (Dallas,TX)
def convert_city_to_coords(waypoints):
	waypoint_results = []
	result = ""

	with open('uscities', 'rb') as f:
		cities = pickle.load(f)
	for waypoint in waypoints:
		# check if first character in waypoint is numeric in which case we treat it as a coord
		if waypoint[0].isnumeric():
			waypoint_results.append(waypoint)
			# skip the remainder of the loop since we know this is a coord
			continue
		else:
			# strip white space and make it lower to match the keys
			waypoint = waypoint.strip().lower().split(",")
			waypoint = ''.join(waypoint)
		if waypoint in cities.keys():
			waypoint_results.append(cities[waypoint])
		else:
			return False
	return waypoint_results

# Retrieves the aircraft from the pickle and creates a generator which is then
# converted to a python dict and returned the first index. somehow it's a list within a list
# so we just get the 0 index which is all the data

def convert_aircraft_to_python_object():
	# load pickle into generator
	vessels = loadall('aircraft')
	# convert generator object to dict
	vessels_dict = list(vessels)
	if(len(vessels_dict) > 0):
		return vessels_dict[0]
	else:
		return []

# Writes aircraft python object passed in to python pickle file aircraft
def write_aircraft(aircraft_to_write):
	w_file = open('aircraft', 'wb')
	pickle.dump(aircraft_to_write, w_file)

# loads all pickle data from aircraft file into python object
def loadall(file_name):
	with open(file_name, "rb") as r_file:
		while True:
			try:
				yield pickle.load(r_file)
			except EOFError:
				break

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

# it's like it is getting the right waypoint index but the waypoint it measures from 
# when it hits the end of the track is wrong and keeps changing. 

# try it with three waypoints to see if it makes the turn right - also check the source waypoint
# for the calculations 
