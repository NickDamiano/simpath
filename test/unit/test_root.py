from test.unit import client
import pdb
import app
from modules import calculate_position

# def test_landing(client):
# 	landing = client.get("/")
# 	assert landing.status_code == 200
aircraft_backup = ""

# captures original pickle file, clear the file for the tests so that 
# actual contents don't interfere with tests and tests are consistent
def setup():
	print("Starting Setup - backing up Aircraft file")
	all_aircraft = app.convert_aircraft_to_python_object()
	app.write_aircraft([])
	return all_aircraft

# tests creation of 1 aircraft
def test_create_aircraft(client):
	rv = client.post('/CreateAircraft', json=[
	{
		"name": "clipclop",
		"altitude": 10000,
		"aircraft_type": "F-18",
		"cruising_speed": 450,
		"start_time": None,
		"waypoints": [{"latitude": 33.128416, "longitude": -117.280023},{"latitude": 34.918010, "longitude": -117.891509}]
	}
	])
	json_data = rv.get_json()
	test_aircraft = json_data[-1]
	assert rv.status_code == 201
	assert test_aircraft["name"] == "clipclop"
	assert test_aircraft["altitude"] == 10000
	assert test_aircraft["aircraft_type"] == "F-18"
	assert test_aircraft["cruising_speed"] == 450
	assert test_aircraft["start_time"] == None

# Test creation of multiple aircraft and 
def test_create_multiple_aircraft(client):
	test_aircraft = [
	{ "name": "Hog 71", "aircraft_type": "A-10", "altitude": 1000, "cruising_speed": 565, "start_time": None, "waypoints": [
	{"latitude": 32.744512, "longitude": -96.969403},
	{"latitude": 33.108040, "longitude": -96.607846}
	]},
	{ "name": "Hog 72", "aircraft_type": "A-10", "altitude": 1000, "cruising_speed": 565, "start_time": None, "waypoints": [
	{"latitude": 32.744512, "longitude": -96.969403},
	{"latitude": 33.108040, "longitude": -96.607846}
	]},
	{ "name": "Slasher 93", "aircraft_type": "AC-130", "altitude": 1000, "cruising_speed": 565, "start_time": None, "waypoints": [
	{"latitude": 32.744512, "longitude": -96.969403},
	{"latitude": 33.108040, "longitude": -96.607846}
	]},
	{ "name": "Bone 19", "aircraft_type": "B-1", "altitude": 1000, "cruising_speed": 565, "start_time": None, "waypoints": [
	{"latitude": 32.744512, "longitude": -96.969403},
	{"latitude": 33.108040, "longitude": -96.607846}
	]}
	]
	rv = client.post('/CreateAircraft', json=test_aircraft)
	assert rv.status_code == 201
	json_data = rv.get_json()
	assert len(json_data) == 5

# test getting all aircraft data
def test_get_all_aircraft(client):
	all_aircraft = client.get('/GetAllAircraft')
	json_data = all_aircraft.get_json()
	assert len(json_data) == 5

def test_correct_convert_city_to_coords():
	converted_coords = app.convert_city_to_coords(["Austin,TX"])
	assert converted_coords[0] == "30.3005,-97.7522"

def test_incorrect_convert_city_to_coords():
	converted_coords = app.convert_city_to_coords(["Lasertown,TX"])
	assert converted_coords == False

# should return the same coordinated passed in
def test_correct_coords_city_to_coords():
	test_coords = "33.1234,-98.1234"
	converted_coords = app.convert_city_to_coords([test_coords])
	assert converted_coords[0] == test_coords

# tests starting a single aircraft
def test_start_by_name(client):
	rv = client.post('/start', json={
		"aircraft_names": ["clipclop"]
	})
	json_data = rv.get_json()
	assert json_data["start_time"] != ""

# tests getting all aircraft positions
def test_all_aircraft_positions(client):
	rv = client.get('/AllAircraftPositions')
	all_aircraft = rv.get_json()
	assert len(all_aircraft) == 1

def tests_calculate_distance():
	start_lat 	= 38.1234
	start_long 	= -98.1234
	end_lat 	= 39.1234
	end_long 	= -99.1234
	distance = calculate_position.calculate_distance(start_lat,start_long,end_lat,end_long)
	distance_rounded = round(distance, 2)
	assert distance_rounded == 87.67

#restore pickle aircraft file
def restore():
	print("Starting Teardown - restoring original Aircraft file")
	app.write_aircraft(aircraft_backup)

# add test for calculate position methods
# calculate which gets projected point
# calculate bearing
# calculate_distance