from test.unit import client
import pdb
import app

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

#restore pickle aircraft file
def restore():
	print("Starting Teardown - restoring original Aircraft file")
	app.write_aircraft(aircraft_backup)