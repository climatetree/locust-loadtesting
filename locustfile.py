from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    # def on_start(self):
    #     """ on_start is called when a Locust start before
    #         any task is scheduled
    #     """
    #     self.login()
    #
    # def login(self):
    #     self.client.post("/login",
    #                      {"username":"ellen_key",
    #                       "password":"education"})

    @task(1)
    def index(self):
        self.client.get("/stories")

    @task(2)
    def login(self):
        self.client.post("/login",  {"username":"shwetamandavgane123","email":"mandavgane@gmail.com"})


    @task(3)
    def profile(self):
        # self.client.get("/profile")
        self.client.get("/stories")
        # stories microservice
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories?page=1&limit=100")
        # need a new story id
        #self.client.get("https://backend-mongo-stories.azurewebsites.net/stories/story/5e3899c5463a27ee9a334781")
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories/place/1")
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories/title/china?page=1&limit=1")
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories/topStories/3")
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories/comment")

        # places microservice
        self.client.get("https://places-postgres2.azurewebsites.net/api/places/:searchTerm")
        self.client.get("https://places-postgres2.azurewebsites.net/api/places/3233/similar")
        self.client.get("https://places-postgres2.azurewebsites.net/api/places/3233/similar/advanced?populationStart=80&populationEnd=110&carbonStart=90&carbonEnd=200&perCapCarbonStart=70&perCapCarbonEnd=130&popDensityStart=50&popDensityEnd=150")
        self.client.get("https://places-postgres2.azurewebsites.net/api/places/nearest?latitude=42&longitude=-72")
        
        # user microservice
        self.client.get("https://user-microservice-demo.herokuapp.com/user")
        # how to test login
        # self.client.get("https://user-microservice-demo.herokuapp.com/login")
        self.client.get("https://usermicroservice-climatetree.azurewebsites.net/user/searchname?name=shwetamandavgane123")
        self.client.get("https://usermicroservice-climatetree.azurewebsites.net/user/searchname?name=shwetamandavgane123")
        self.client.get("https://usermicroservice-climatetree.azurewebsites.net/user/searchrole?roleid=3")
        
        # self.client.put("https://usermicroservice-climatetree.azurewebsites.net/user/")
        # self.client.post("https://usermicroservice-climatetree.azurewebsites.net/user/addUser")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000