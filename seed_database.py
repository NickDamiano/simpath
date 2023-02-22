import pickle

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

stream = open('aircraft', 'wb')
pickle.dump(test_aircraft, stream)