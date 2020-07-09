from dataclasses import dataclass
from datetime import datetime

from plexapi.server import PlexServer
from plexapi.video import Episode, Movie

MAXIMUM_TITLE_LENGTH = 22

@dataclass
class PlexStream:
    show_name: str
    episode_name: str
    episode_number: str
    movie_name: str
    time_left: int
    is_tv_stream: bool


def get_plex_stream_details(plex_url: str, plex_token: str) -> PlexStream:
    p_server = PlexServer(baseurl=plex_url, token=plex_token)

    if not p_server.sessions():
        print("No Streaming Sessions, Exiting....")
        raise BaseException("No Streaming Sessions Active")
    current_session = p_server.sessions()[0]
    if not isinstance(current_session, Episode) and not isinstance(current_session, Movie):
        print("Invalid Media Stream Found, Exiting....")
        raise BaseException("Invalid Media Stream Found")

    is_tv_stream = isinstance(current_session, Episode)
    now = datetime.now()
    show_name = ""
    episode_name = ""
    episode_number = ""
    movie_name = ""
    time_left = now.timestamp() + ((current_session.duration - current_session.viewOffset) / 1000)
    if is_tv_stream:
        show_name = current_session.grandparentTitle
        episode_name = current_session.title
        if len(current_session.title) > MAXIMUM_TITLE_LENGTH:
            episode_name = f"{current_session.title[0:MAXIMUM_TITLE_LENGTH]}..."
        episode_number = current_session.seasonEpisode.upper()
    else:
        movie_name = current_session.originalTitle

    return PlexStream(
        show_name=show_name,
        episode_name=episode_name,
        episode_number=episode_number,
        is_tv_stream=is_tv_stream,
        time_left=time_left,
        movie_name=movie_name
    )
