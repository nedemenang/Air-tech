import json
from locust import HttpLocust, TaskSet, task


class AppTaskSet(TaskSet):
    
    def on_start(self):
        self.login()

    def login(self):
        data = {'emailAddress': 'nnamso.edemenang@gmail.com', 'password': 'Password1'}
        json_data = json.dumps(data)
        response = self.client.post("/api/v1/user/login/", json_data, headers={'Content-Type': 'application/json'})
        self.token = json.loads(response._content).get('token')

    @task(1)
    def get_flights(self):
        self.client.get("/api/v1/flight/", headers={'Authorization': 'bearer {}'.format(self.token)})

    @task(2)
    def get_a_flight(self):
        self.client.get("/api/v1/flight/1", headers={'Authorization': 'bearer {}'.format(self.token)})

    @task(3)
    def get_tickets(self):
        self.client.get("/api/v1/ticket/", headers={'Authorization': 'bearer {}'.format(self.token)})

    @task(4)
    def get_a_ticket(self):
        self.client.get("/api/v1/ticket/1/", headers={'Authorization': 'bearer {}'.format(self.token)})


class WebsiteUser(HttpLocust):
    task_set = AppTaskSet
    min_wait = 4000
    max_wait = 8000
