import pickle

test_aircraft = { "name": "buttercup", "aircraft_type": "KC-10", "altitude": 1000, "cruising_speed": 565, "start_time": None, "waypoints": [
 {"latitude": 32.744512, "longitude": -96.969403},
 {"latitude": 33.108040, "longitude": -96.607846}
]}

stream = open('aircraft', 'wb')
pickle.dump(test_aircraft, stream)