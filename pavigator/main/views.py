from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import EmailSerializers,StopSerializers,StopTimeSerializers
from .models import EmailModel,StopModel,StopTimeModel,TripModel,CalenderModel,NodeModel
from datetime import datetime, timedelta
from django.http import JsonResponse
import re,json,requests,math,random,subprocess
from .api_key import api_key
from celery import shared_task,Celery
from .routing import Routing
from geopy import distance
from  .route import RouteMST
from celery.result import AsyncResult


# Create your views here.
@api_view(['GET'])
def usersList(request):
	user = EmailModel.objects.all()
	serializer = EmailSerializers(user,many=True)
	return Response(serializer.data)

@api_view(['GET'])
def specificUser(request,indentifier):
	user = EmailModel.objects.get(email=indentifier)
	serializer = EmailSerializers(user,many=False)
	return Response(serializer.data)

@api_view(['POST'])
def CreateUser(request):
	try:
		email = EmailModel.objects.get(email=request.data["email"])
		return Response("User Exists")
	except EmailModel.DoesNotExist:
		serializer = EmailSerializers(data=request.data)
		if serializer.is_valid():
			serializer.save()
		return Response("User Successfully Created")

@api_view(['POST'])
def UpdateUser(request, identifier):
	try:
		user = EmailModel.objects.get(email=identifier)
		if user.password == request.data["password"]:
			return Response("Successfully SignedIn")
		return Response("Wrong Password")
	except EmailModel.DoesNotExist:
		return Response("No User Present with Email")
		# serializer = EmailSerializers(instance=user, data=request.data, many=True)

@api_view(['GET','DELETE'])
def DeleteUser(request, identifier):
	user = EmailModel.objects.get(email=identifier)
	user.delete()
	return Response("User Successfully Deleted")

@api_view(['GET'])
def TimeTable(request, StopNumber):
	StopNumber = f"Stop {StopNumber}"
	now = datetime.now().strftime('%H:%M:%S');
	later = (datetime.now() + timedelta(minutes=45)).strftime('%H:%M:%S')
	stop = StopModel.objects.filter(stopName__iendswith=StopNumber).first()
	if stop:
		service_ids =  [service.serviceID for service in CalenderModel.objects.filter(**{datetime.now().strftime('%A').lower(): '1'})]

		routes = StopTimeModel.objects.filter(
			stopID=stop,
			scheduledArrivalTime__range=(now,later),
			tripID__in=TripModel.objects.filter(serviceID__in=service_ids)
		)
		trips = [
			{
				'TripID': route.tripID.tripID,
				'scheduledArrivalTime': 0 if getMinutes(route.scheduledArrivalTime) <= 1 else getMinutes(route.scheduledArrivalTime)
			} 
			for route in routes
		]
		trips.sort(key=TripSort)

		for trip in trips:
			mtch = tripIDToShortName(trip["TripID"])
			start, end = mtch.span()
			start += 1
			end -= 1
			trip["Bus"] = trip["TripID"][start:end]
		
		for trip in trips:
			if trip["scheduledArrivalTime"] == 0:
				trip["scheduledArrivalTime"] = "Soon"

		return Response({"TimeTable":trips,"Stop":"Stop " + StopNumber})

	return Response({"TimeTable":[]})
def getMinutes(scheduledArrivalTime):
	time_obj1 = datetime.strptime(scheduledArrivalTime, "%H:%M:%S")
	time_obj2 = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")

	time_diff = abs(time_obj1 - time_obj2)

	return math.ceil(time_diff.seconds / 60)

def tripIDToShortName(trip):
	return re.search(r"[-][A-Z0-9]*[-]", trip)

def TripSort(e):
	return e['scheduledArrivalTime']


@shared_task(name="update_arrivaltime")
def run_update_arrivaltime():
	api_response  = httpRequest()
	if api_response.status_code != 200:
		return "Sorry Error Occurred."

	api_response =  api_response.json()
	for entity in api_response["Entity"]:
		tripID = entity["Id"]
		try:
			for timeUpdate in entity["TripUpdate"]["StopTimeUpdate"]:
				if not StopTimeModel.objects.filter(tripID_id=tripID,stopID_id=timeUpdate["StopId"]).exists():
					continue
				current=StopTimeModel.objects.get(tripID_id=tripID,stopID_id=timeUpdate["StopId"])
				if current:
					try:
						newCurrentTime = datetime.strptime(current.arrivalTime, "%H:%M:%S") + timedelta(seconds=int(timeUpdate['Arrival']["Delay"]))
						current.scheduledArrivalTime = newCurrentTime.strftime("%H:%M:%S")
						current.save(update_fields=['scheduledArrivalTime'])
						print(str(timeUpdate["StopId"]) +" "+ tripID +" " + str(current.arrivalTime )+"---->" + str(newCurrentTime.strftime("%H:%M:%S")) +" " + str(timeUpdate['Arrival']["Delay"] )+ " has updated arrival time")
					except KeyError:
						pass
		except KeyError:
			print("No StopTimeUpdate")

def httpRequest():
    __URL = "https://api.nationaltransport.ie/gtfsr/v1?format=json"
    __HEADERS = {
    "Cache-control":"no-cache",
    "x-api-key":api_key,
    "text":"application/json"        
    }
    return requests.get(__URL,headers=__HEADERS)

def GeoCoding(address):
	__URL = "https://us1.locationiq.com/v1/search"
	__DATA = {
		'key': 'pk.2e90a13902cf34408f4cbdbba5b58980',
		'q': address,
		'format': 'json'
	}
	response = requests.get(__URL, params=__DATA)
	return (response.json()[0]["lat"],response.json()[0]["lon"])

@api_view(['POST'])
def RouteMapping(request):
	points = request.data
	origin = GeoCoding(points["origin"])
	destination = GeoCoding(points["destination"])

	stop_within_200_origin = []
	stop_within_200_destination = []
	for stop in StopModel.objects.all():
		if(longDistance((stop.stopLat, stop.stopLon), origin)) < 0.5:
			stop_within_200_origin.append(stop.stopID)
		if(longDistance((stop.stopLat, stop.stopLon), destination)) < 0.5:
			stop_within_200_destination.append(stop.stopID)

	closet_stop_origin = stopCoordinates(stop_within_200_origin[0])
	closet_stop_destination = stopCoordinates(stop_within_200_destination[0])

	closet_stop_origin = (closet_stop_origin[0],closet_stop_origin[1])
	closet_stop_destination = (closet_stop_destination[0],closet_stop_destination[1])

	extras = []
	start_walk = []
	begin = Routing([[origin[1],origin[0]],[closet_stop_origin[1],closet_stop_origin[0]]])["paths"][0]
	for i in begin["points"]["coordinates"]:
		start_walk.append([i[1],i[0]])
	extras.append({"Walk":math.ceil((begin["time"]/(1000*60))%60)})#math.ceil((begin["time"]/(1000*60))%60)
	
	coord = []
	coords = []
	djikistra_nodes = MST(stop_within_200_origin[0], stop_within_200_destination[0])
	print(djikistra_nodes)
	for stop in range(len(djikistra_nodes) - 1):
		start = StopModel.objects.filter(stopID=djikistra_nodes[stop]).values_list("stopLat", "stopLon",flat=False)[0]
		end = StopModel.objects.filter(stopID=djikistra_nodes[stop+1]).values_list("stopLat", "stopLon",flat=False)[0]
		for ds in Routing([[start[1],start[0]],[end[1],end[0]]])["paths"][0]["points"]["coordinates"]:
			coord.append(ds)

	for i in list(coord):
		coords.append([i[1],i[0]])

	end_walk = []
	end = Routing([[closet_stop_destination[1],closet_stop_destination[0]],[destination[1],destination[0]]])["paths"][0]
	for i in end["points"]["coordinates"]:
		end_walk.append([i[1],i[0]])
	extras.append({"Walk":math.ceil((end["time"]/(1000*60))%60)})#math.ceil((end["time"]/(1000*60))%60)

	return Response({"start":start_walk,"end":end_walk, "Location":coords, "extras":extras})

def longDistance(point1, point2):
	return distance.distance(point1, point2).km

def routes_within(location):
	return set(StopTimeModel.objects.filter
		(stopID_id__in=location).values_list('tripID__tripID', flat=True)
	)

def stopCoordinates(stop):
	return StopModel.objects.filter(stopID=stop).values_list("stopLat", "stopLon",flat=False).first()

def stripStop(name):
	return re.search('[0-9]+$', name)

# def mst_djiksitra():
# 	stops = StopModel.objects.all().values_list('stopID', flat=True)
# 	graph = {stop:{} for stop in stops}
# 	for stop in stops:
# 		for trip in StopTimeModel.objects.filter(stopID=stop).values_list('tripID_id', flat=True):
# 			node = StopTimeModel.objects.filter(tripID_id=trip).values_list('stopID_id', flat=True)
# 			nodes = StopTimeModel.objects.filter(tripID_id=trip).values_list('shapeDistTravelled', flat=True)
# 			vertices = [float(nodes[0])]
# 			for i in range(1,len(nodes)):
# 				diff = float(nodes[i]) - float(vertices[-1])
# 				vertices.append(diff)
# 			for ver in range(len(node)):
# 				graph[stop][node[ver]] = vertices[ver]

# 	for stop in graph.keys():
# 		for innerKey in graph[stop].keys():
# 			node = NodeModel(start=stop, end=innerKey, distance=graph[stop][innerKey])
# 			node.save()

def mst_djiksitra():
	stops = StopModel.objects.all().values_list('stopID', flat=True)
	for stop in stops:
		for trip in StopTimeModel.objects.filter(stopID=stop).values_list('tripID_id', flat=True):
			nodes = [ node for node in StopTimeModel.objects.filter(
				tripID_id=trip
			).values_list('stopID_id','shapeDistTravelled', flat=False)]
			for i in range(len(nodes)-1):
				node = NodeModel(start=nodes[i][0], end=nodes[(i+1)][0], distance=float(nodes[(i+1)][1])-float(nodes[i][1]))
				node.save()
			
def MST(source, destination):
	graph = {}
	for node in NodeModel.objects.all().values_list('start', 'end', 'distance'):
	# Add the edge to the graph dictionary
		if node[0] not in graph:
			graph[node[0]] = {}
		else:
			graph[node[0]][node[1]] = node[2]

	return RouteMST(graph, source, destination)

# print(print(NodeModel.objects.order_by('start').distinct("start")))
# print(MST("8220DB000167","8220DB000183"))






