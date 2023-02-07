from modules import calculate_position as position
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import pdb
import yaml
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

@app.route('/start', methods=['POST'])
def start_flying():
	# identify the aircraft name from keys passed
	aircraft_name 	= request.args.get('aircraft_name')

	# open the yaml file to read, load the yaml to be a python object
	stream = open('aircraft.yaml', 'r+')
	vessels = yaml.load_all(stream)
	
	# find the vessel name we are starting, set current time (time since epoch)
	for vessel in vessels:
		# pdb.set_trace()
		if(vessel["name"] == aircraft_name):
			vessel["start_time"] = time.time()

	yaml.dump(vessels, stream)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

# arg1=value1&arg2=value2
# print(result1)
# print(result2)

