from modules import calculate_position as position
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import pdb
import pickle
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
	# lat = request.args.get('lat')
	# print(lat)
	new_long, new_lat = position.calculate(35.79225921965943,-103.36822768355603,500,45)
	return jsonify({'longitude': new_long, 'latitude': new_lat })

@app.route('/calculate_coords', methods=['POST'])
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
	vessels = loadall('aircraft')

	# convert generator object to dict
	pdb.set_trace()
	vessels_dict = {vessel.name:vessel.value for vessel in vessels}

	# # open the file to read, load the file to be a python object
	# r_file = open('aircraft', 'rb')
	# vessels = pickle.load(r_file)
	# r_file.close()
	
	# find the vessel name we are starting, set current time (time since epoch)
	for vessel in vessels_dict:
		if(vessel["name"] == aircraft_name):
			start_time = time.time()
			vessel["start_time"] = start_time

	w_file = open('aircraft', 'wb')
	pickle.dump(vessels_dict, w_file)
	return jsonify({"aircraft_name": aircraft_name, "start_time": start_time})

def loadall(file_name):
	with open(file_name, "rb") as r_file:
		while True:
			try:
				yield pickle.load(r_file)
			except EOFError:
				break

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

# arg1=value1&arg2=value2
# print(result1)
# print(result2)

