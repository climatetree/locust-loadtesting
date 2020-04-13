from locust import HttpLocust, TaskSet, task
import json

class UserBehavior(TaskSet):
	@task(1)
	def places_test(self):
		self.client.get("https://places-postgres2.azurewebsites.net/api/places/:searchTerm")
		self.client.get("https://places-postgres2.azurewebsites.net/api/places/3233/similar")
		self.client.get("https://places-postgres2.azurewebsites.net/api/places/3233/similar/advanced?populationStart=80&populationEnd=110&carbonStart=90&carbonEnd=200&perCapCarbonStart=70&perCapCarbonEnd=130&popDensityStart=50&popDensityEnd=150")
		self.client.get("https://places-postgres2.azurewebsites.net/api/places/nearest?latitude=42&longitude=-72")

class WebsiteUser(HttpLocust):
	task_set = UserBehavior
	min_wait = 5000
	max_wait = 9000