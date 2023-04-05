from django.db import models
# Create your models here.

class StopModel(models.Model):
	class Meta:
		app_label = 'main'
	stopID = models.CharField(max_length=255,primary_key=True)
	stopName = models.CharField(max_length=255)
	stopLat = models.CharField(max_length=255)
	stopLon = models.CharField(max_length=255)

class AgencyModel(models.Model):
	class Meta:
		app_label = 'main'
	agencyID = models.CharField(max_length=255,primary_key=True)
	agencyName = models.CharField(max_length=255)
	agencyUrl = models.CharField(max_length=255)
	agencyTimeZone = models.CharField(max_length=255)
	agencyLang = models.CharField(max_length=255)
	agencyPhone = models.CharField(max_length=255)

class RouteModel(models.Model):
	class Meta:
		app_label = 'main'
	routeID = models.CharField(max_length=255,primary_key=True)
	agencyID = models.ForeignKey(AgencyModel, on_delete=models.CASCADE)
	routeShortName = models.CharField(max_length=255)
	routeLongName = models.CharField(max_length=255)	
	routeType = models.CharField(max_length=255)	

class CalenderModel(models.Model):
	class Meta:
		app_label = 'main'
	serviceID = models.CharField(max_length=255, primary_key=True)
	monday = models.CharField(max_length=255)
	tuesday = models.CharField(max_length=255)
	wednesday = models.CharField(max_length=255)
	thursday = models.CharField(max_length=255)
	friday = models.CharField(max_length=255)
	saturday = models.CharField(max_length=255)
	sunday = models.CharField(max_length=255)
	startDate = models.CharField(max_length=255)
	endDate = models.CharField(max_length=255)

class ShapeModel(models.Model):
	class Meta:
		app_label = 'main'
	shapeID = models.CharField(max_length=255, primary_key=True)
	shapePtLat = models.CharField(max_length=255)
	shapePtLon = models.CharField(max_length=255)
	shapePtSequence = models.CharField(max_length=255)
	shapeDistTravelled = models.CharField(max_length=255)

class TripModel(models.Model):
	class Meta:
		app_label = 'main'
	routeID = models.ForeignKey(RouteModel, on_delete=models.CASCADE)
	serviceID = models.ForeignKey(CalenderModel, on_delete=models.CASCADE)
	tripID = models.CharField(max_length=255,primary_key=True)
	shapeID = models.ForeignKey(ShapeModel, on_delete=models.CASCADE)
	tripHeadSign = models.CharField(max_length=255)
	directionID = models.CharField(max_length=255)	

class EmailModel(models.Model):
	class Meta:
		app_label = 'main'
	email = models.CharField(max_length=255,primary_key=True)
	password = models.CharField(max_length=255)
	lastName = models.CharField(max_length=255)
	firstName = models.CharField(max_length=255)

class TripTakenModel(models.Model):
	class Meta:
		app_label = 'main'
	id = models.AutoField(primary_key=True, default = 1)
	email = models.ForeignKey(EmailModel, on_delete=models.CASCADE)
	stopID = models.ForeignKey(StopModel, on_delete=models.CASCADE)
	tripID = models.ForeignKey(TripModel, on_delete=models.CASCADE)

class StopTimeModel(models.Model):
	class Meta:
		app_label = 'main'
	id = models.AutoField(primary_key=True, default = 1)
	tripID = models.ForeignKey(TripModel, on_delete=models.CASCADE)
	arrivalTime = models.CharField(max_length=255)
	scheduledArrivalTime = models.CharField(max_length=255)
	departureTime = models.CharField(max_length=255)
	stopID = models.ForeignKey(StopModel, on_delete=models.CASCADE)
	stopSequence = models.CharField(max_length=255)
	stopHeadSign = models.CharField(max_length=255)
	pickUpType = models.CharField(max_length=255)
	dropOffType = models.CharField(max_length=255)
	shapeDistTravelled = models.CharField(max_length=255)

class TransfersModel(models.Model):
	class Meta:
		app_label = 'main'
	id = models.AutoField(primary_key=True, default = 1)
	fromStopID = models.ForeignKey(StopModel, on_delete=models.CASCADE, related_name='transfers_from_stop')
	toStopID = models.ForeignKey(StopModel, on_delete=models.CASCADE, related_name='transfers_to_stop')
	transferType = models.CharField(max_length=255)
	minTransferTime = models.CharField(max_length=255)

class CalendarDatesModel(models.Model):
	class Meta:
		app_label = 'main'
	id = models.AutoField(primary_key=True, default = 1)
	serviceID = models.ForeignKey(CalenderModel, on_delete=models.CASCADE)
	date = models.CharField(max_length=255)
	exceptionType = models.CharField(max_length=255)

class NodeModel(models.Model):
	start = models.CharField(max_length=255)
	end = models.CharField(max_length=255)
	distance = models.FloatField()