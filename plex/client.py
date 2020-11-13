from datetime import datetime

from plexapi.server import PlexServer
from plexapi.video import Episode, Movie

from plex.exceptions import InvalidStreamException, StreamsNotFoundException, InvalidParameterException
from plex.stream import PlexStream


class PlexConnection(object):
    MAXIMUM_TITLE_LENGTH = 22
    p_server = None

    def __init__(self,
                 url: str,
                 token: str
                 ):
        """Initializes the class

        :param url: Plex URL (https://localhost:32400)
        :param token: Plex User Token
        """
        self.url = url
        self.token = token
        super(object).__init__()

    def get_plex_stream_details(self, plex_username: str) -> PlexStream:
        if not plex_username:
            print("Plex username not supplied to get_plex_stream_details!")
            raise InvalidParameterException("No Streaming Sessions Active")

        if not self.p_server:
            self.p_server = PlexServer(baseurl=self.url, token=self.token)

        for current_session in self.p_server.sessions():
            if not isinstance(current_session, Episode) and not isinstance(current_session, Movie):
                print("Invalid Media Stream Found, Exiting....")
                raise InvalidStreamException("Invalid Media Stream Found")
            if plex_username not in current_session.usernames:
                print(f"{plex_username} not found in active stream")
                continue

            is_tv_stream = isinstance(current_session, Episode)
            now = datetime.now()
            show_name = ""
            episode_name = ""
            episode_number = ""
            movie_name = ""
            director = ""
            year = current_session.year
            time_left = now.timestamp() + ((current_session.duration - current_session.viewOffset) / 1000)
            if is_tv_stream:
                show_name = current_session.grandparentTitle
                episode_name = current_session.title
                if len(current_session.title) > self.MAXIMUM_TITLE_LENGTH:
                    episode_name = f"{current_session.title[0:self.MAXIMUM_TITLE_LENGTH]}..."
                episode_number = current_session.seasonEpisode.upper()
            else:
                movie_name = current_session.title
                if len(current_session.directors):
                    director = current_session.directors[0].tag

            return PlexStream(
                show_name=show_name,
                episode_name=episode_name,
                episode_number=episode_number,
                is_tv_stream=is_tv_stream,
                time_left=time_left,
                year=year,
                movie_name=movie_name,
                director=director
            )
        raise StreamsNotFoundException(f"No Streaming Sessions Active for {plex_username}")
