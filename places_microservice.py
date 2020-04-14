from locust import HttpLocust, TaskSet, task
import json
from random import randint

class UserBehavior(TaskSet):
	@task(1)
	def places_test(self):
		cities = ['Seattle','Nagpur', 'Boston', 'Brookhaven', 'Hendley', 'Plandome', 'Wing', 'Mio', 'Riceville', 'Hollymead', 'Aiea']
		self.client.get("https://places-postgres2.azurewebsites.net/api/v1/places/"+cities[randint(0,10)])

class WebsiteUser(HttpLocust):
	task_set = UserBehavior
	min_wait = 5000
	max_wait = 9000