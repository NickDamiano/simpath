from test.unit import client
import pdb
import app
from modules import calculate_position

#SETUP
# captures original pickle file, clear the file for the tests so that 
# actual contents don't interfere with tests and tests are consistent
print("Starting Setup - backing up Aircraft file")
aircraft_backup = app.convert_aircraft_to_python_object()
# erase test file
with open("aircraft",'w') as file:
    pass

# tests creation of 1 aircraft
def test_create_aircraft(client):
	rv = client.post('/CreateAircraft', json=[
	{
		"name": "clipclop",
		"altitude": 10000,
		"aircraft_type": "F-18",
		"cruising_speed": 450,
		"start_time": None,
		"waypoints": ["33.128416,-117.280023","34.918010,-117.891509"]
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
	 "32.744512,-96.969403", "33.108040,-96.607846"
	]},
	{ "name": "Hog 72", "aircraft_type": "A-10", "altitude": 1000, "cruising_speed": 565, "start_time": None, "waypoints": [
	 "32.744512,-96.969403","33.108040,-96.607846"
	]},
	{ "name": "Slasher 93", "aircraft_type": "AC-130", "altitude": 1000, "cruising_speed": 565, "start_time": None, "waypoints": [
	"32.744512,-96.969403","33.108040,-96.607846"
	]},
	{ "name": "Bone 19", "aircraft_type": "B-1", "altitude": 1000, "cruising_speed": 565, "start_time": None, "waypoints": [
	"32.744512,-96.969403","33.108040,-96.607846"
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

# # not working
# def test_start_all(client):
# 	rv = client.post('/startAll')
# 	json_data = rv.get_json()
# 	assert json_data["start_time"] != ""

def test_calculate_segment_start_and_bearing():
	# test for distance between second and third waypiont
	# waypoints, RGAAF, Lampasas, Lake buchanan back to hood, roughly 81 miles
	waypoints = ["31.064421,-97.829107","31.064094,-98.181702","30.826594,-98.418648"]

	distance_traveled = 0
	index_of_segment_start, bearing = app.calculate_segment_start_and_bearing(waypoints, distance_traveled)
	assert index_of_segment_start == 0
	

	distance_traveled = 5443
	index_of_segment_start, bearing = app.calculate_segment_start_and_bearing(waypoints, distance_traveled)
	assert index_of_segment_start == 0

	distance_traveled = 30000
	index_of_segment_start, bearing = app.calculate_segment_start_and_bearing(waypoints, distance_traveled)
	assert index_of_segment_start == 1

	distance_traveled = 70000
	index_of_segment_start, bearing = app.calculate_segment_start_and_bearing(waypoints, distance_traveled)
	assert index_of_segment_start == 2

def test_calculate_bearing():
	start_lat 	= "38.1234"
	start_long 	= -98.1234
	end_lat 	= 39.1234
	end_long 	= -99.1234
	bearing = calculate_position.calculate_bearing(start_lat, start_long, end_lat, end_long)
	assert int(bearing) == 322

	bearing = calculate_position.calculate_bearing(end_lat, end_long,start_lat, start_long)
	assert int(bearing) == 141

def test_calculate_distance():
	start_lat 	= "38.1234"
	start_long 	= -98.1234
	end_lat 	= 39.1234
	end_long 	= -99.1234
	distance = calculate_position.calculate_distance(start_lat,start_long,end_lat,end_long)
	distance_int = int(distance)
	assert distance_int == 87

def test_roundtrip_distance():
	waypoints = ["4.704659,-74.069079","4.077158,-73.563053","0.742613,-75.237578"]
	roundtrip_distance = app.calculate_roundtrip_distance(waypoints)
	assert int(roundtrip_distance) == 959315

#restore pickle aircraft file
def test_restore():
	print("Starting Teardown - restoring original Aircraft file")
	app.write_aircraft(aircraft_backup)

# add test to stop by name
# not handling when trying to start by name and name doesn't exist	
# add test to stop all 
# add test to wipe all aircraft from the file
# add test to stop by name
# add test to stop all
# add test for calculate position methods
# calculate which gets projected point
# calculate_distance