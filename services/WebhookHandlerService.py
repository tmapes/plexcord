from datetime import datetime

import models
from config import AppConfig
from utils.Constants import *
from . import PresenceService


class WebhookHandlerService:
    _VALID_EVENTS = [MEDIA_PLAY, MEDIA_STOP, MEDIA_PAUSE, MEDIA_RESUME]
    _VALID_EVENT_TYPES = [MOVIE_EVENT_TYPE, EPISODE_EVENT_TYPE]

    def __init__(self, config: AppConfig, presence_svc: PresenceService):
        self.config = config
        self.presence_svc = presence_svc

    def process_hook(self, webhook: dict):
        if not self._should_process(webhook):
            return

        plex_stream = models.PlexStreamData.from_dict(webhook)

        if plex_stream.no_longer_watching():
            self.presence_svc.clear_presence()
        elif plex_stream.starting_watch():

            if plex_stream.is_media_play():
                end_time = int(datetime.now().timestamp() + (plex_stream.length / 1000))
            else:
                end_time = int(datetime.now().timestamp() + ((plex_stream.length - plex_stream.view_offset) / 1000))

            self.presence_svc.set_presence(plex_stream, end_time)

    def _should_process(self, webhook: dict) -> bool:
        monitored_user: str = self.config.plex_username == webhook.get('Account', {}).get('title')
        if not monitored_user:
            print("Event did not originate from the monitored user, skipping")
            return False

        event_type: str = webhook.get('event', '')
        if event_type not in self._VALID_EVENTS:
            print(f"'{event_type}' not in allowed events, skipping")
            return False

        metadata: dict = webhook.get('Metadata', {})
        if not metadata:
            print(f'Did not find Metadata for this event, skipping')
            print(webhook)
            return False

        media_type: str = metadata.get('type', '')
        if media_type not in self._VALID_EVENT_TYPES:
            print(f"'{media_type}' not an allowed media type, skipping")
            return False

        return True
