from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
	@task(1)
	def places_test(self):
		self.client.get("https://climatetree-api-gateway.azurewebsites.net/geoserver/wfs?service=wfs&version=2.0.0&request=GetFeature&typeNames=ClimateTree:Similar_Places&outputFormat=application/json&viewparams=TYPE_ID_2:2;POPULATION_LOW:4000;POPULATION_HIGH:500000")

class WebsiteUser(HttpLocust):
	task_set = UserBehavior
	min_wait = 5000
	max_wait = 9000