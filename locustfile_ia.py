import random

from locust import HttpUser, between, task
from client import SocialMediaClient


# Probabilites de transition estimees a partir des logs.
# Chaque ligne correspond a l'etat actuel et chaque colonne a l'etat suivant.
TRANSITIONS = {
    "feed": {
        "profile": 0.177650,
        "like": 0.673352,
        "post": 0.148998,
    },
    "profile": {
        "feed": 0.319635,
        "follow": 0.680365,
    },
    "like": {
        "feed": 0.311966,
        "profile": 0.688034,
    },
    "follow": {
        "feed": 1.0,
    },
    "post": {
        "feed": 1.0,
    },
}


class MarkovSocialMediaUser(HttpUser):
    """
    Simule un utilisateur du reseau social avec une chaine de Markov.

    Une iteration execute l'action correspondant a l'etat courant,
    puis choisit le prochain etat selon la matrice de transition.
    """

    wait_time = between(1, 5)

    def on_start(self):
        self.social_media_client = SocialMediaClient(self.client)
        self.social_media_client.login()

        # Dans les logs, la premiere action apres la connexion est GET /feed.
        self.current_state = "feed"

    def _choose_next_state(self):
        transitions = TRANSITIONS[self.current_state]
        next_states = list(transitions.keys())
        probabilities = list(transitions.values())

        self.current_state = random.choices(
            next_states,
            weights=probabilities,
            k=1,
        )[0]

    @task
    def execute_markov_action(self):
        if self.current_state == "feed":
            self.social_media_client.view_feed()

        elif self.current_state == "profile":
            self.social_media_client.view_profile()

        elif self.current_state == "like":
            self.social_media_client.like_post()

        elif self.current_state == "follow":
            self.social_media_client.follow_user()

        elif self.current_state == "post":
            self.social_media_client.create_post()

        self._choose_next_state()
