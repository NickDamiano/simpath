# SimPath
A Python Flask API to return geocoordinates for 1 or more simulated aircraft moving between user-defined waypoints

Use case: 
1. I need to have an api to query to show multiple aircraft flying on a map - specifically to simulate military aircraft flying between waypoints for 
a demonstration at satellite communications trade shows when simulating passing aircraft positional data passed over multiple hops through black and red side.
2. I want to initally use python pickles to store the aircraft data for purposes of deploying this app to various servers with personnel who are non-technical
3. I want to send a json file as a post request to set the aircraft to fly
4. I want to use both lat long and US city state as mixed waypoints if desired or all us city or all lat long waypoints
5. I want to query to start individual aircraft by name 
6. I want to query to start all aircraft in aircraft file

# Instructions:
After launching the flask app.py

## Add aircraft to database
send post request to /CreateAircraft with body 
```
[
    {
        "name": "clipclop",
        "altitude": 10000,
        "aircraft_type": "F-18",
        "cruising_speed": 450,
        "start_time": null,
        "waypoints": [{"latitude": 33.128416, "longitude": -117.280023},{"latitude": 34.918010, "longitude": -117.891509}]
    }
]
```
With one or more aircraft

## Start aircraft by name
Post request to /start 
```
{
    "aircraft_names": ["clipclop"]
}
```
where names is a list of aircraft names to start. This sets the current time to epoch used when calculated
distance traveled so far to project the coordinate it would be at that time.

## Get all Aircraft positions
Get request to /AllAircraftPositions
Returns json file showing aircraft name and current coordinates

## Get all aircraft in database
Gets aircraft name, waypoints, distance bearing, etc (not current position)
get request to /GetAllAircraft
