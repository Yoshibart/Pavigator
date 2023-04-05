from django.contrib import admin

# Register your models here.
from .models import StopModel,TripModel,RouteModel,EmailModel,TripTakenModel,StopTimeModel,TransfersModel,CalendarDatesModel,CalenderModel,AgencyModel,NodeModel
admin.site.register(StopModel)
admin.site.register(TripModel)
admin.site.register(RouteModel)
admin.site.register(EmailModel)
admin.site.register(TripTakenModel)
admin.site.register(StopTimeModel)
admin.site.register(TransfersModel)
admin.site.register(CalendarDatesModel)
admin.site.register(CalenderModel)
admin.site.register(AgencyModel)
admin.site.register(NodeModel)