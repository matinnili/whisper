import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hello_world(self):
        response=self.client.post("/api/v1/whisper", files={"file": ("test.mp3", open("/mnt/locust/test.mp3", "rb"), "audio/mp3")})
        if response.status_code != 200:
                return
            task_id = response.json().get("task_id")

        # Poll the result until it's ready
        for _ in range(10):
            result = self.client.get(f"/result/{task_id}")
            if result.status_code == 200 and "text" in result.json():
                break
            time.sleep(1)



