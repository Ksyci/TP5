from locust import task, between, MarkovTaskSet, transition, User, HttpUser
from client import SocialMediaClient

class ExampleTaskSet(MarkovTaskSet):
    def __init__(self, user: User):
        super().__init__(user)
        self.social_media_client = SocialMediaClient(self.client)

    def on_start(self):
        self.social_media_client.login()

    @transition("like_post", weight=235)
    @transition("view_profile", weight=62)
    @transition("create_post", weight=52)
    def view_feed(self):
        self.social_media_client.view_feed()

    @transition("view_profile", weight=161)
    @transition("view_feed", weight=73)
    def like_post(self):
        self.social_media_client.like_post()

    @transition("follow_user", weight=149)
    @transition("view_feed", weight=70)
    def view_profile(self):
        self.social_media_client.view_profile()

    @transition("view_feed", weight=148)
    def follow_user(self):
        self.social_media_client.follow_user()

    @transition("view_feed", weight=52)
    def create_post(self):
        self.social_media_client.create_post()

class ExampleSocialMediaUser(HttpUser):
    wait_time = between(1, 5)
    tasks = [ExampleTaskSet]
