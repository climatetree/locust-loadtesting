from locust import HttpLocust, TaskSet, task
import json

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before
            any task is scheduled
        """
        self.token = self.login()
        self.headers = {'Authorization': 'Bearer ' + self.token}
        self.all_ids = []

    def on_stop(self):
        #serach all test users by name
        by_name = self.client.get("https://usermicroservice-climatetree.azurewebsites.net/v1/user/searchname/temp_user", headers=self.headers)
        users = by_name.json()["users"]
        for x in users:
            if (x["userId"] not in self.all_ids):
        	    self.all_ids.append(x["userId"])
        #delete all test_users
        for x in self.all_ids:
            delete_url = "http://usermicroservice-climatetree.azurewebsites.net/v1/user/" + str(x)
            self.client.delete(delete_url, headers = self.headers)


    #create user 
    #successful login 
    def login(self):
        response = self.client.post("https://usermicroservice-climatetree.azurewebsites.net/v1/user/login", json={
            "username":"load_test_user",
            "email":"load_test_user@gmail.com"
        })
        return json.loads(response._content)['jwtToken']

    @task(1)
    def user_lifetime(self):

        #create another user
        test_user = self.client.post("https://usermicroservice-climatetree.azurewebsites.net/v1/user/login", json={
            "username":"temp_user",
            "email":"temp_user@gmail.com"
        })

        #unauthorized login 
        with self.client.post('https://usermicroservice-climatetree.azurewebsites.net/login',json={"username":"load_test_user", "email":"<load_test_user@gmail.com>"}, catch_response=True) as unauthorized:
            if (unauthorized.status_code==401):
                unauthorized.success()

        #method not allow
        with self.client.post('https://usermicroservice-climatetree.azurewebsites.net/v1/user/login1',json={"username":"load_test_user", "email":"<load_test_user@gmail.com>"}, catch_response=True) as method:
            if (method.status_code==405):
                method.success()

        #serach user by name
        by_name = self.client.get("https://usermicroservice-climatetree.azurewebsites.net/v1/user/searchname/temp_user", headers=self.headers)
        user_id = str(by_name.json()["users"][0]["userId"])

        # serach user by role
        role_url = "https://usermicroservice-climatetree.azurewebsites.net/v1/user/searchrole/3"
        self.client.get(role_url, headers = self.headers)

        #search user by email
        self.client.get("https://usermicroservice-climatetree.azurewebsites.net/v1/user/searchemail/temp_user@gmail.com", headers=self.headers)

        #search blacklisted user
        self.client.get("https://usermicroservice-climatetree.azurewebsites.net/v1/user/flagged_users")

        #update user role 
        update_url = "http://usermicroservice-climatetree.azurewebsites.net/v1/user/" + user_id + "/2"
        self.client.put(update_url, headers = self.headers)

        # black list user 
        baned_user_url = "http://usermicroservice-climatetree.azurewebsites.net/v1/user/blacklist/" + user_id
        self.client.put(baned_user_url, headers=self.headers)

        # unblacklist
        unbaned_user_url = "http://usermicroservice-climatetree.azurewebsites.net/v1/user/unblacklist/" + user_id
        self.client.put(unbaned_user_url, headers=self.headers)

        #request role change 
        role_change_url = "http://usermicroservice-climatetree.azurewebsites.net/v1/user/request_role_change/" + user_id + "/2"
        self.client.post("http://usermicroservice-climatetree.azurewebsites.net/v1/user/request_role_change/3/2", headers=self.headers)

        # get all role change requests
        self.client.get("https://usermicroservice-climatetree.azurewebsites.net/v1/user/get_all_role_update_requests", headers=self.headers)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000