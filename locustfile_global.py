from locust import HttpUser, task, between
from client import SocialMediaClient

class QuickStartUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.social_client = SocialMediaClient(self.client)
        self.social_client.login()

    @task(353)
    def view_feed(self):
        self.social_client.view_feed()

    @task(52)
    def create_post(self):
        self.social_client.create_post()

    @task(235)
    def like_post(self):
        self.social_client.like_post()

    @task(149)
    def follow_user(self):
        self.social_client.follow_user()

    @task(223)
    def view_profile(self):
        self.social_client.view_profile()