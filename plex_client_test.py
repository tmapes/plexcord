from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from freezegun import freeze_time
from plexapi.video import Episode, Movie

from plex_client import PlexStream, get_plex_stream_details


class PlexClientTest(TestCase):

    def setUp(self) -> None:
        self.plex_token = "token"
        self.plex_url = "http://localhost:32400"

    @patch('plexapi.server.PlexServer.__new__')
    def test_no_sessions_raises_exception(self, mock_plex_server):
        with patch('plexapi.server.PlexServer.__new__') as MockPlexServer:
            MockPlexServer.return_value = mock_plex_server
            mock_plex_server.sessions.return_value = []

            try:
                get_plex_stream_details(plex_url=self.plex_url, plex_token=self.plex_token)
                self.fail("Expected Exception to be thrown")
            except BaseException as ex:
                self.assertEqual("No Streaming Sessions Active", str(ex))
            MockPlexServer.assert_called_once()
            mock_plex_server.sessions.assert_called_once()

    @patch('plexapi.server.PlexServer.__new__')
    def test_invalid_session_instance_raises_exception(self, mock_plex_server):
        with patch('plexapi.server.PlexServer.__new__') as MockPlexServer:
            MockPlexServer.return_value = mock_plex_server
            mock_plex_server.sessions.return_value = ["string"]

            try:
                get_plex_stream_details(plex_url=self.plex_url, plex_token=self.plex_token)
                self.fail("Expected Exception to be thrown")
            except BaseException as ex:
                self.assertEqual("Invalid Media Stream Found", str(ex))
            MockPlexServer.assert_called_once()
            self.assertEqual(2, mock_plex_server.sessions.call_count)

    @freeze_time(time_to_freeze="2020-01-02")
    @patch('plexapi.server.PlexServer.__new__')
    def test_session_valid_tv_show(self, mock_plex_server):
        start_time = datetime(year=2020, month=1, day=1)
        expected_plex_stream = PlexStream(movie_name="", show_name="Rick & Morty", is_tv_stream=True,
                                          episode_number="S01E01", episode_name="Pilot",
                                          start_time=int(start_time.timestamp()))

        with patch('plexapi.server.PlexServer.__new__') as MockPlexServer:
            MockPlexServer.return_value = mock_plex_server
            episode = Episode(mock_plex_server, None)
            episode.grandparentTitle = "Rick & Morty"
            episode._seasonNumber = 1
            episode.index = 1
            episode.title = "Pilot"
            episode.viewOffset = 1000 * 60 * 60 * 24
            mock_plex_server.sessions.return_value = [episode]

            output = get_plex_stream_details(plex_url=self.plex_url, plex_token=self.plex_token)
            self.assertEqual(expected_plex_stream, output)

            MockPlexServer.assert_called_once()
            self.assertEqual(2, mock_plex_server.sessions.call_count)

    @freeze_time(time_to_freeze="2020-01-02")
    @patch('plexapi.server.PlexServer.__new__')
    def test_session_valid_movie(self, mock_plex_server):
        start_time = datetime(year=2020, month=1, day=1)
        expected_plex_stream = PlexStream(movie_name="Rick & Morty the Movie",
                                          show_name="",
                                          is_tv_stream=False,
                                          episode_number="",
                                          episode_name="",
                                          start_time=int(start_time.timestamp()))

        with patch('plexapi.server.PlexServer.__new__') as MockPlexServer:
            MockPlexServer.return_value = mock_plex_server
            movie = Movie(mock_plex_server, None)
            movie.originalTitle = "Rick & Morty the Movie"
            movie.viewOffset = 1000 * 60 * 60 * 24
            mock_plex_server.sessions.return_value = [movie]

            output = get_plex_stream_details(plex_url=self.plex_url, plex_token=self.plex_token)
            self.assertEqual(expected_plex_stream, output)

            MockPlexServer.assert_called_once()
            self.assertEqual(2, mock_plex_server.sessions.call_count)
