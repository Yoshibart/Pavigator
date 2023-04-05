import requests

def Routing(points):
  url = "https://graphhopper.com/api/1/route"
  query = {
    "key": "cd389932-b12d-4578-beb9-153b1d570fe3"
  }

  payload = {
    "points":points,
    "snap_preventions": [ "motorway", "ferry", "tunnel"],
    "details": [ "road_class", "surface"],
    "vehicle": "car",
    "locale": "en",
    "instructions": True,
    "calc_points": True,
    "points_encoded": False
  }

  headers = {"Content-Type": "application/json"}

  response = requests.post(url, json=payload, headers=headers, params=query)

  return response.json()

def getTimes(stop):
  response = requests.get(f'http://127.0.0.1:8000/timetable/{stop}')
  if response.status_code == 200:
    return response.json()
  return []