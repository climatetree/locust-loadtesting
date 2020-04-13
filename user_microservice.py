from locust import HttpLocust, TaskSet, task
import json

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before
            any task is scheduled
        """
        self.token = self.login()
        self.headers = {'Authorization': 'Bearer ' + self.token}

    #create user 
    #successful login 
    def login(self):
        response = self.client.post("https://usermicroservice-climatetree.azurewebsites.net/user/login", json={
            "username":"load_test_user",
            "email":"<load_test_user@gmail.com>"
        })
        return json.loads(response._content)['jwtToken']


    @task(1)
    def user_lifetime(self):
        #unauthorized login 
        with self.client.post('https://usermicroservice-climatetree.azurewebsites.net/login',json={"username":"load_test_user", "email":"<load_test_user@gmail.com>"}, catch_response=True) as unauthorized:
            if (unauthorized.status_code==401):
                unauthorized.success()

        #method not allow
        with self.client.post('https://usermicroservice-climatetree.azurewebsites.net/user/login1',json={"username":"load_test_user", "email":"<load_test_user@gmail.com>"}, catch_response=True) as method:
            if (method.status_code==405):
                method.success()

        #serach user by name
        by_name = self.client.get("https://usermicroservice-climatetree.azurewebsites.net/user/searchname", json={
            "username":"load_test_user"
        }, headers=self.headers)
        print(by_name.json())

        #search user by role
        self.client.get("https://usermicroservice-climatetree.azurewebsites.net/user/searchrole", json={
            "roleId":3
        })

        #search user by email
        self.client.get("https://usermicroservice-climatetree.azurewebsites.net/user/searchemail", json={
            "email":"<load_test_user@gmail.com>"
        }, headers=self.headers)

        #search blacklisted user
        self.client.get("https://usermicroservice-climatetree.azurewebsites.net/user/flagged_users")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000