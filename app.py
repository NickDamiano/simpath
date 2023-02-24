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

# Takes a json file with 1 or more aircraft, pulls the existing planes, appends the new planes to it and saves it. 
@app.route('/CreateAircraft', methods=['POST'])
def create_aircraft():
	# Load pickle data of existing aircraft and convert to python dict/object
	all_aircraft = convert_aircraft_to_python_object()

	# parse the json file passed in
	new_aircraft = request.get_json()

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
		waypoints = all_aircraft[0]["waypoints"]


		# current time minus start time * 0.514444 (knots to meters per second) times the speed of the aircraft
		# 	= distance traveled converted to integer
		if aircraft["start_time"] != None:	
			# Calculate distance traveled
			distance_traveled = int((time.time() - aircraft["start_time"]) * (aircraft["cruising_speed"] * .514444))

			# pass the waypoints and distance to helper function, which figures out the start point
			# 	and returns the bearing of travel, point to measure from, and distance from that point

			


			# current bearing is coordinates[0],coordinates[1] passed to calculate bearing
			start_point = aircraft["waypoints"][0]
			end_point = aircraft["waypoints"][1]
			current_bearing = position.calculate_bearing(start_point["latitude"], start_point["longitude"], 
				end_point["latitude"], end_point["longitude"])
			new_long, new_lat = position.calculate(start_point["latitude"], start_point["longitude"],distance_traveled / 1000,current_bearing)
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

# Takes an array of waypoints, a distance traveled, and calculates which segments the aircraft would be on
# then returns the latlong for last waypoint completed, bearing from that origin point, and distance forward
def calculate_segment_start_and_bearing(waypoints, distance):
	# rebuild the array with latlong only (convert city state)
	# first import uscities.csv in chunks
	print('test')

	# determine waypoint type, city state or latlong

	# set lat long variables
	# 

def convert_city_to_coords(waypoints):
	chunk = pd.read_csv('uscities.csv', chunksize=1000)
	df = pd.concat(chunk)
	pdb.set_trace()

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

# method i started writing to calculate specific positions
# takes url params list of aircraft names
# @app.route('/get_aircraft_position', methods=["GET"])
# def get_positions():
# 	names = request.args.get("names")
# 	names_list = names.split(",")
# 	for name in names_list:
# 		distance = calculate_distance(name)


# # Test method to make sure calculation works - Delete
# @app.route('/', methods=['GET'])
# def test():
# 	# lat = request.args.get('lat')
# 	# print(lat)
# 	new_long, new_lat = position.calculate(35.79225921965943,-103.36822768355603,500,45)
# 	return jsonify({'longitude': new_long, 'latitude': new_lat })


# next either write more tests or work making it work for as many waypoints as user wants.
