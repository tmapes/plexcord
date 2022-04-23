from pypresence import Presence, utils

import models
from config import AppConfig


class PresenceService:

    def __init__(self, config: AppConfig):
        self.config = config
        self.presence_client: Presence = None
        self._create_pipe()

    def __del__(self):
        self._clear_client()

    def clear_presence(self):
        self._create_pipe()
        if not self.presence_client:
            return

        try:
            self.presence_client.clear(self.config.discord_process_id)
        except Exception as e:
            print('Failed to clear')
            print(e)
            self._clear_client()

    def set_presence(self, plex_stream: models.PlexStreamData, end_time: int):
        self._create_pipe()

        try:
            self.presence_client.update(
                pid=self.config.discord_process_id,
                details=plex_stream.get_plex_details(),
                state=plex_stream.get_plex_state(),
                end=end_time
            )
        except:
            self._clear_client()
            print('Failed to set presence')

    def _create_pipe(self):
        if self.presence_client is not None:
            return

        print('Creating presence client')
        try:
            # TODO, remove custom loop https://github.com/qwertyquerty/pypresence/issues/164
            self.presence_client = Presence(self.config.discord_client_id, pipe=0, loop=utils.get_event_loop(True))
            self.presence_client.connect()
            print('Client created on pipe 0')
        except BaseException as e:
            print('Discord Client Exception')
            print(e)
            self._clear_client()

    def _clear_client(self):
        print('Closing Discord Client')
        try:
            self.presence_client.close()
        finally:
            self.presence_client = None
