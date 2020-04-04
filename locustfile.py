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


    @task(1)
    def profile(self):
        self.client.get("/profile")
        

    @task(1)
    def story_lifetime(self):
        #create a story
        story = self.client.post("https://backend-mongo-stories.azurewebsites.net/stories/create", json={
        "user_id" : 323,
        "hyperlink" : "https://ipcc.ch/climate/",
        "posted_by" : "test_user",
        "rating" : 3,
        "story_title" : "News report",
        "place_ids" : [
            3,
            5
        ],
        "media_type" : "video",
        "date" : "01/18/2014 01:12 AM",
        "solution" : [
            "LED Lighting (Household)",
            "Landfill Methane",
            "Landfill Methane"
        ],
        "sector" : "Materials",
        "comments" : [
            {
                "comment_id" : 1,
                "user_id" : 203,
                "content" : "bad post",
                "date" : "12/16/2016 05:24 AM"
            },
            {
                "comment_id" : 2,
                "user_id" : 404,
                "content" : "good post",
                "date" : "05/22/2013 07:01 AM"
            },
            {
                "comment_id" : 3,
                "user_id" : 421,
                "content" : "very informative",
                "date" : "12/22/2013 03:39 AM"
            }
        ]
        })

        story_id = story.json()["story_id"]
        user_id = str(story.json()["user_id"])
        print(story_id)

        #find story by story id 
        story_url = "https://backend-mongo-stories.azurewebsites.net/stories/story/" + story_id
        self.client.get(story_url)

        #find a story by title
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories/title/china?page=1&limit=1")

        #update story 
        update_url = "https://backend-mongo-stories.azurewebsites.net/stories/update/" + story_id
        self.client.put(update_url, data={
            "place_ids": [
                3,
                5,
                7,
                10
            ]
        })

        #like story
        like_url = "https://backend-mongo-stories.azurewebsites.net/stories/" + story_id + "/like/" + user_id
        self.client.put(like_url)

        #unlike story
        unlike_url = "https://backend-mongo-stories.azurewebsites.net/stories/" + story_id + "/unlike/" + user_id
        self.client.put(unlike_url)


        #update rating of a story 
        url = "https://backend-mongo-stories.azurewebsites.net/stories/rating/update"
        self.client.put(url, json={
            "storyID": "5e8919e9545da9001217bb3f",
            "role": 1,
            "rating": 5
        })

        #add comment 
        # add comment api temporarily has issue 
        # add_commend_url = "https://backend-mongo-stories.azurewebsites.net/stories/story/comment"
        # self.client.post(add_commend_url， json={
        #     "user_id" : 323,
        #     "story_id" : "5e890b2d545da9001217b2c8", 
        #     "content" : "comemnt",
        #     "date" : "01/18/2014 01:12 AM",
        #     "username" “ 
        #     })

        #delete a comment 
        # delete_comment_url = "" 
        # self.client.delete()

        #delete a story 
        delete_url = "https://backend-mongo-stories.azurewebsites.net/stories/delete/" + story_id
        self.client.delete(delete_url)

        #find a story by place id
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories?page=1&limit=100")
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories/place/1")
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories/topStories/3")

        #find all comemnts
        self.client.get("https://backend-mongo-stories.azurewebsites.net/stories/comment")


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