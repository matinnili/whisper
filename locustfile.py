import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hello_world(self):
        self.client.post("/api/v1/whisper", files={"file": ("test.mp3", open("/mnt/locust/test.mp3", "rb"), "audio/mp3")})



