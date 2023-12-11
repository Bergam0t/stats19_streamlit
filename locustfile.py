from locust import HttpUser, task, between

class SimpleUser(HttpUser):
    @task
    def load_page(self):
        self.client.get("/")

    wait_time = between(30, 120)

class PointUser(HttpUser):
    @task
    def load_page(self):
        self.client.get("/Point_Map")
    wait_time = between(30, 120)

class ChoroplethUser(HttpUser):
    @task
    def load_page(self):
        self.client.get("/Choropleth")
    wait_time = between(30, 120)