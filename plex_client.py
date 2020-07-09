from dataclasses import dataclass
from datetime import datetime

from plexapi.server import PlexServer
from plexapi.video import Episode, Movie


@dataclass
class PlexStream:
    show_name: str
    episode_name: str
    episode_number: str
    movie_name: str
    start_time: int
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
    start_time = int(now.timestamp()) - (current_session.viewOffset / 1000)
    show_name = ""
    episode_name = ""
    episode_number = ""
    movie_name = ""
    if is_tv_stream:
        show_name = current_session.grandparentTitle
        episode_name = current_session.title
        episode_number = current_session.seasonEpisode.upper()
    else:
        movie_name = current_session.originalTitle

    return PlexStream(
        show_name=show_name,
        episode_name=episode_name,
        episode_number=episode_number,
        is_tv_stream=is_tv_stream,
        start_time=start_time,
        movie_name=movie_name
    )
