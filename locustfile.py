from locust import HttpLocust, TaskSet, task
import json

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    def login(self):
        response = self.client.post("/v1/auth/login", json.dumps({
            "email": "luro@mailmetal.com",
            "password": "password"
        }))

        self.token = response.json()['data']['token']

    @task(1)
    def create_flight(self):
        response = self.client.post(
            "/v1/flights",
            json.dumps({
                'estimated_arrival_time': '2014-12-22T03:12:58.019077+00:00',
                'airline': 'Arik',
                'departure_time': '2014-12-22T03:12:58.019077+00:00',
                'fare': 50000,
                'max_capacity': 40,
                'destination': 'Enugu',
                'origin': 'Calabar'
            }),
            headers={
                'Authorization': 'Bearer ' + self.token
            },
        )

        self.flight_id = response.json()['data']['flight']['id']

    @task(2)
    def get_flights(self):
        self.client.get("/v1/flights", headers={
            'Authorization': 'Bearer ' + self.token
        })

    @task(3)
    def book_flight(self):
        self.client.post(
            '/v1/flights/5d14bc4fd6296537305d54cd/book',
            headers={
                'Authorization': 'Bearer ' + self.token
            },
        )

    @task(4)
    def get_bookings(self):
        self.client.get(
            '/v1/flights/5d14bc4fd6296537305d54cd/bookings',
            headers={
                'Authorization': 'Bearer ' + self.token
            },
        )

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
