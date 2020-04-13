from locust import HttpLocust, TaskSet, task
import json

class UserBehavior(TaskSet):
    @task(1)
    def index(self):
        #get all stories
        self.client.get("/stories")
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories?page=1&limit=100")


    @task(1)
    def story_lifetime(self):

        #create a story
        story = self.client.post("https://backend-mongo-stories.azurewebsites.net/v1/stories/create", json={
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

        #find story by story id 
        story_url = "https://backend-mongo-stories.azurewebsites.net/v1/stories/story/" + story_id
        self.client.get(story_url)

        #find a story by title
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/title/china?page=1&limit=1")

        #update story 
        update_url = "https://backend-mongo-stories.azurewebsites.net/v1/stories/update/" + story_id
        self.client.put(update_url, data={
            "place_ids": [
                3,
                5,
                7,
                10
            ]
        })

        #like story
        like_url = "https://backend-mongo-stories.azurewebsites.net/v1/stories/" + story_id + "/like/" + user_id
        self.client.put(like_url)

        #unlike story
        unlike_url = "https://backend-mongo-stories.azurewebsites.net/v1/stories/" + story_id + "/unlike/" + user_id
        self.client.put(unlike_url)


        #update rating of a story 
        url = "https://backend-mongo-stories.azurewebsites.net/v1/stories/rating/update"
        self.client.put(url, json={
            "storyID": story_id,
            "role": 1,
            "rating": 5
        })

        # add comment 
        # add comment api temporarily has issue 
        # add_commend_url = "https://backend-mongo-stories.azurewebsites.net/stories/story/comment"
        # self.client.post(add_commend_url， json={
        #     "user_id" : 323,
        #     "story_id" : "5e890b2d545da9001217b2c8", 
        #     "content" : "comemnt",
        #     "date" : "01/18/2014 01:12 AM",
        #     "username" “ 
        #     })

        # delete a comment 
        # delete_comment_url = "" 
        # self.client.delete()

        # find a story by place id
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories?page=1&limit=100")
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/place/1")
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/topStories/3")

        # find all comemnts
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/comment")

        # find top n storeis 
        # where n = 5
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/topStories/5")

        # flag a story
        self.client.put("https://backend-mongo-stories.azurewebsites.net/v1/stories/" + story_id +"/flag/" + user_id)

        # unflag a story
        self.client.put("https://backend-mongo-stories.azurewebsites.net/v1/stories/" + story_id +"/unflag/" + user_id)


        # delete a story 
        delete_url = "https://backend-mongo-stories.azurewebsites.net/v1/stories/delete/" + story_id
        self.client.delete(delete_url)

    @task(1)
    def global_scale(self):
        #get a preview of webpage
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/getPreview?hyperlink=https://www.google.com")

        # find all unrated story
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/unrated?page=1&limit=20")

        # find all stories by solution
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/solution/wiki?page=1&limit=20")

        # find all stoies by sector
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/solution/?page=1&limit=20")

        # find all stoies by stretegy
        self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/solution/:strategy?page=1&limit=20")

        # get all media types (future)
        # self.client.get("https://backend-mongo-stories.azurewebsites.net/v1/stories/mediaTypes")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000