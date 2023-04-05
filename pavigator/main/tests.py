from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from django.urls import reverse
from .models import EmailModel, NodeModel
from .views import MST,CreateUser
from .serializer import EmailSerializers

class CreateUserTestCase(APITestCase):
    def setUp(self):
    	self.client = APIClient()
    	self.email = "barnet@obeka.ie"
    	self.data = {"email": self.email,"password": "password456","lastName":"obeka","firstName":"barnet"}
    	self.url = f"http://localhost:8000/create/"
    	
    def test_create_user_successfully(self):
    	response = self.client.post(self.url, self.data)
    	self.assertEqual(response.status_code, 200)
    	self.assertEqual(response.data, "User Successfully Created")

    def test_create_user_already_exists(self):
    	EmailModel.objects.create(email=self.email, password="password789", lastName="obeka", firstName="barnet")
    	response = self.client.post(self.url, self.data)
    	self.assertEqual(response.status_code, 200)
    	self.assertEqual(response.data, "User Exists")

class LoginUserTestCase(APITestCase):
	def setUp(self):
		self.client = APIClient()
		self.identifier = "barnet@obeka.com"
		self.password = "password789"
		self.url= f"http://localhost:8000/update/{self.identifier}"
		
	def test_update_user_with_correct_password(self):
		EmailModel.objects.create(email=self.identifier, password="password789", lastName="obeka", firstName="barnet")
		data = {"email": self.identifier,"password": "password789"}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, "Successfully SignedIn")

	def test_update_user_with_wrong_password(self):
		EmailModel.objects.create(email=self.identifier, password="password789", lastName="obeka", firstName="barnet")
		data = {"email": self.identifier,"password": "password456"}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, "Wrong Password")

	def test_update_user_with_invalid_email(self):
		data = {"email": "james@bond.uk", "password": "password789"}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, "No User Present with Email")

class RouteMSTTestCase(APITestCase):
	def setUp(self):
		NodeModel.objects.create(start="A", end="B", distance=1)
		NodeModel.objects.create(start="A", end="C", distance=3)
		NodeModel.objects.create(start="B", end="C", distance=2)
		NodeModel.objects.create(start="B", end="D", distance=4)
		NodeModel.objects.create(start="C", end="D", distance=5)
		NodeModel.objects.create(start="D", end="B", distance=6)
		NodeModel.objects.create(start="D", end="A", distance=7)

	def test_route_mst_A_C(self):
		mst = MST("A", "C")
		self.assertEqual(mst, ['A','C'])
		
	def test_route_mst_B_C(self):
		mst = MST("B", "C")
		self.assertEqual(mst, ['B', 'D', 'A', 'C'])


