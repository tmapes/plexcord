from dataclasses import dataclass

from utils.Constants import *


@dataclass
class PlexStreamData:
    # Movie name or Episode Name
    title: str
    year: int
    event_type: str
    # milliseconds
    length: int
    # milliseconds, only populated on resume events
    view_offset: int
    # is this a TV Show Episode
    is_show: bool
    # only populated when is_show is True
    show_name: str
    # only populated when is_show is True
    episode_number: int
    # only populated when is_show is True
    season_number: int

    def get_plex_details(self) -> str:
        if self.is_show:
            return f'{self.show_name} S{self.season_number:02}E{self.episode_number:02}'
        return self.title

    def get_plex_state(self) -> str:
        if self.is_show:
            return self.title
        return str(self.year)

    def is_media_play(self) -> bool:
        return self.event_type == MEDIA_PLAY

    def is_media_pause(self) -> bool:
        return self.event_type == MEDIA_PAUSE

    def is_media_stop(self) -> bool:
        return self.event_type == MEDIA_STOP

    def is_media_resume(self) -> bool:
        return self.event_type == MEDIA_RESUME

    def no_longer_watching(self) -> bool:
        return self.is_media_pause() or self.is_media_stop()

    def starting_watch(self) -> bool:
        return self.is_media_play() or self.is_media_resume()

    @staticmethod
    def from_dict(values: dict) -> 'PlexStreamData':
        metadata: dict = values.get('Metadata', {})
        is_episode = metadata.get('type', '') == 'episode'

        show_name = ''
        episode_number = -1
        season_number = -1
        if is_episode:
            show_name = metadata.get('grandparentTitle', '')
            season_number = metadata.get('parentIndex', -1)
            episode_number = metadata.get('index', -1)

        return PlexStreamData(
            title=metadata.get('title', ''),
            year=metadata.get('year', metadata.get('parentYear', 1970)),
            event_type=values.get('event', ''),
            show_name=show_name,
            is_show=is_episode,
            episode_number=episode_number,
            season_number=season_number,
            length=metadata.get('duration', 3_600_000),
            view_offset=metadata.get('viewOffset', 0)
        )
