from modules import calculate_position as position
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import pdb
import pickle
import time


app = Flask(__name__)

# Test method to make sure calculation works - Delete
@app.route('/', methods=['GET'])
def test():
	# lat = request.args.get('lat')
	# print(lat)
	new_long, new_lat = position.calculate(35.79225921965943,-103.36822768355603,500,45)
	return jsonify({'longitude': new_long, 'latitude': new_lat })

# Returns all aircraft positions in json object
@app.route('/AllAircraftPositions', methods=["GET"])
def get_all_positions():
	distance_traveled = 0
	current_bearing = ""
	aircraft_results = []
	all_aircraft = convert_aircraft_to_python_object()
	for aircraft in all_aircraft:
		# current time minus start time * 0.514444 (knots to meters per second) times the speed of the aircraft
		# 	= distance traveled converted to integer
		distance_traveled = int((time.time() - aircraft["start_time"]) * (aircraft["cruising_speed"] * .514444))
		# current bearing is coordinates[0],coordinates[1] passed to calculate bearing
		start_point = aircraft["waypoints"][0]
		end_point = aircraft["waypoints"][1]
		current_bearing = position.calculate_bearing(start_point["latitude"], start_point["longitude"], 
			end_point["latitude"], end_point["longitude"])
		new_long, new_lat = position.calculate(start_point["latitude"], start_point["longitude"],distance_traveled,current_bearing)

	return jsonify(current_bearing)
	# iterate through all aircraft, if the time stamp isnt' blank then 
	# calculate distance traveled
	# calculate bearing between the points
	# calculate new position
	# add aircraft name and position to dictionary
	# after loop return dictionary as json


# returns calculation of new position with explicitly passed in paramters
@app.route('/calculate_coords', methods=['GET'])
def set_aircraft_data():
	latitude 	= float(request.args.get('latitude'))
	longitude 	= float(request.args.get('longitude'))
	distance	= float(request.args.get('distance'))
	bearing		= float(request.args.get('bearing'))

	new_lat, new_long = position.calculate(latitude,longitude,distance,bearing)
	return jsonify({'latitude': new_lat, 'longitude': new_long })

@app.route('/getallaircraft', methods=['GET'])
def print_all_aircraft():
	# open the file to read, load the file to be a python object
	file = open('aircraft', 'rb')
	vessels = pickle.load(file)
	
	# find the vessel name we are starting, set current time (time since epoch)
	return jsonify(vessels)

@app.route('/start', methods=['POST'])
def start_flying():
	start_time = ""
	# identify the aircraft name from keys passed
	aircraft_name 	= request.args.get('aircraft_name')
	vessels_dict = convert_aircraft_to_python_object()

	# find the vessel name we are starting, set current time (time since epoch)
	for vessel in vessels_dict:
		if(vessel["name"] == aircraft_name):
			start_time = time.time()
			vessel["start_time"] = start_time

	w_file = open('aircraft', 'wb')
	pickle.dump(vessels_dict, w_file)
	return jsonify({"aircraft_name": aircraft_name, "start_time": start_time})

# helper methods
def convert_aircraft_to_python_object():
	# load pickle into generator
	vessels = loadall('aircraft')

	# convert generator object to dict
	vessels_dict = list(vessels)
	return vessels_dict[0]

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


# where was i? now i can update the time stamp so next step is to write a method that calculates the distance traveled in meters and returns
# that and that is passed to the position.calculate new lat long. possibly write a method that is like get_position that has a url property for name 
# of the aircraft. 
# then take multiple names and calculate multiple positions and return those as json object. then record a demo showing a script
# calling the api and updating a file that google earth is looking at. look back at the thing Cody 