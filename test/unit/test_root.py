from test.unit import client
import pdb

# def test_landing(client):
# 	landing = client.get("/")
# 	assert landing.status_code == 200

def setup:
	#backup pickle

def teardown:
	#restore pickle

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
    # pdb.set_trace()
    test_aircraft = json_data[-1]
    assert rv.status_code == 201
    assert test_aircraft["name"] == "clipclop"
    assert test_aircraft["altitude"] == 10000
    assert test_aircraft["aircraft_type"] == "F-18"
    assert test_aircraft["cruising_speed"] == 450
    assert test_aircraft["start_time"] == None


# def test_start_by_name(client):
# 	rv = client.post('/start')
# 	