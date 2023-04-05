from rest_framework import serializers
from .models import EmailModel
from .models import StopModel
from .models import StopTimeModel

class EmailSerializers(serializers.ModelSerializer):
	class Meta:
		model = EmailModel
		fields = '__all__'

class StopSerializers(serializers.ModelSerializer):
	class Meta:
		model = StopModel
		fields = '__all__'

class StopTimeSerializers(serializers.ModelSerializer):
	class Meta:
		model = StopTimeModel
		fields = '__all__'