import time
from locust import HttpUser, task, between
import logging as log

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hello_world(self):
        result=self.client.get("/api/v1/whisper")
        log.info(f"Response: {result.status_code} - {result.text}")




