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







# def 
# R = 6378.1  #Radius of the Earth
# brng = 1.57  #Bearing is 90 degrees converted to radians.
# d = 1500  #Distance in km

# lat1 = math.radians(36.959530)  #Current lat point converted to radians
# lon1 = math.radians(-120.062866)  #Current long point converted to radians

# lat2 = math.asin(
#   math.sin(lat1) * math.cos(d / R) +
#   math.cos(lat1) * math.sin(d / R) * math.cos(brng))

# lon2 = lon1 + math.atan2(
#   math.sin(brng) * math.sin(d / R) * math.cos(lat1),
#   math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

# lat2 = math.degrees(lat2)
# lon2 = math.degrees(lon2)

# print(lat2)
# print(lon2)


