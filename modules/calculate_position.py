import math
import geopy
import pyproj

from geopy.distance import geodesic


def calculate(lat1, lon1, distance, bearing):
  # given: lat1, lon1, b = bearing in degrees, d = distance in kilometers
  # lat1 = 35.79225921965943
  # lon1 = -103.36822768355603
  # distance = 500
  # bearing = 45
  origin = geopy.Point(lat1, lon1)
  destination = geodesic(kilometers=distance).destination(origin, bearing)

  lat2, lon2 = destination.latitude, destination.longitude
  return lat2, lon2
  print(lat2)
  print(lon2)

def calculate_bearing(lat1, long1, lat2, long2):
  geodesic = pyproj.Geod(ellps='WGS84')
  fwd_azimuth,back_azimuth,distance = geodesic.inv(long1, lat1, long2, lat2)
  return fwd_azimuth


def calculate_distance(lat1, long1, lat2, long2):
  # starthere
  # return distance
  # google if geopy calculates distance between two points
  start = (lat1,long1)
  end   = (lat2,long2)
  distance = geodesic(start,end).miles
  return distance
