from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from freezegun import freeze_time
from plexapi.video import Episode, Movie

from plex import PlexStream, PlexConnection


class PlexClientTest(TestCase):

    def setUp(self) -> None:
        self.plex_token = "token"
        self.plex_url = "http://localhost:32400"
        self.plex = PlexConnection(url=self.plex_url, token=self.plex_token)

    @patch('plexapi.server.PlexServer.__new__')
    def test_no_sessions_raises_exception(self, mock_plex_server):
        with patch('plexapi.server.PlexServer.__new__') as MockPlexServer:
            MockPlexServer.return_value = mock_plex_server
            mock_plex_server.sessions.return_value = []
            try:
                self.plex.get_plex_stream_details()
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
                self.plex.get_plex_stream_details()
                self.fail("Expected Exception to be thrown")
            except BaseException as ex:
                self.assertEqual("Invalid Media Stream Found", str(ex))
            MockPlexServer.assert_called_once()
            self.assertEqual(2, mock_plex_server.sessions.call_count)

    @freeze_time(time_to_freeze="2020-01-01")
    @patch('plexapi.server.PlexServer.__new__')
    def test_session_valid_tv_show(self, mock_plex_server):
        start_time = datetime(year=2020, month=1, day=1, minute=1)
        expected_plex_stream = PlexStream(movie_name="", show_name="Rick & Morty", is_tv_stream=True,
                                          episode_number="S01E01", episode_name="Pilot",
                                          time_left=int(start_time.timestamp()))

        with patch('plexapi.server.PlexServer.__new__') as MockPlexServer:
            MockPlexServer.return_value = mock_plex_server
            episode = Episode(mock_plex_server, None)
            episode.grandparentTitle = "Rick & Morty"
            episode._seasonNumber = 1
            episode.index = 1
            episode.title = "Pilot"
            episode.viewOffset = 0
            episode.duration = 1000 * 60  # 1 Minute
            mock_plex_server.sessions.return_value = [episode]

            output = self.plex.get_plex_stream_details()
            self.assertEqual(expected_plex_stream.movie_name, output.movie_name)
            self.assertEqual(expected_plex_stream.show_name, output.show_name)
            self.assertEqual(expected_plex_stream.is_tv_stream, output.is_tv_stream)
            self.assertEqual(expected_plex_stream.episode_number, output.episode_number)
            self.assertEqual(expected_plex_stream.episode_name, output.episode_name)
            self.assertEqual(expected_plex_stream.time_left, output.time_left)

            MockPlexServer.assert_called_once()
            self.assertEqual(2, mock_plex_server.sessions.call_count)

    @freeze_time(time_to_freeze="2020-01-01")
    @patch('plexapi.server.PlexServer.__new__')
    def test_session_valid_tv_show_length_truncated(self, mock_plex_server):
        start_time = datetime(year=2020, month=1, day=1, minute=1)
        expected_plex_stream = PlexStream(movie_name="", show_name="Rick & Morty", is_tv_stream=True,
                                          episode_number="S01E01", episode_name="Pilot Pilot Pilot Pilo...",
                                          time_left=int(start_time.timestamp()))

        with patch('plexapi.server.PlexServer.__new__') as MockPlexServer:
            MockPlexServer.return_value = mock_plex_server
            episode = Episode(mock_plex_server, None)
            episode.grandparentTitle = "Rick & Morty"
            episode._seasonNumber = 1
            episode.index = 1
            episode.title = "Pilot Pilot Pilot Pilot Pilot"
            episode.viewOffset = 0
            episode.duration = 1000 * 60  # 1 Minute
            mock_plex_server.sessions.return_value = [episode]

            output = self.plex.get_plex_stream_details()
            self.assertEqual(expected_plex_stream.movie_name, output.movie_name)
            self.assertEqual(expected_plex_stream.show_name, output.show_name)
            self.assertEqual(expected_plex_stream.is_tv_stream, output.is_tv_stream)
            self.assertEqual(expected_plex_stream.episode_number, output.episode_number)
            self.assertEqual(expected_plex_stream.episode_name, output.episode_name)
            self.assertEqual(expected_plex_stream.time_left, output.time_left)

            MockPlexServer.assert_called_once()
            self.assertEqual(2, mock_plex_server.sessions.call_count)

    @freeze_time(time_to_freeze="2020-01-01")
    @patch('plexapi.server.PlexServer.__new__')
    def test_session_valid_movie(self, mock_plex_server):
        start_time = datetime(year=2020, month=1, day=1, minute=1)
        expected_plex_stream = PlexStream(movie_name="Rick & Morty the Movie",
                                          show_name="",
                                          is_tv_stream=False,
                                          episode_number="",
                                          episode_name="",
                                          time_left=int(start_time.timestamp()))

        with patch('plexapi.server.PlexServer.__new__') as MockPlexServer:
            MockPlexServer.return_value = mock_plex_server
            movie = Movie(mock_plex_server, None)
            movie.originalTitle = "Rick & Morty the Movie"
            movie.viewOffset = 0
            movie.duration = 1000 * 60
            mock_plex_server.sessions.return_value = [movie]

            output = self.plex.get_plex_stream_details()
            self.assertEqual(expected_plex_stream.movie_name, output.movie_name)
            self.assertEqual(expected_plex_stream.show_name, output.show_name)
            self.assertEqual(expected_plex_stream.is_tv_stream, output.is_tv_stream)
            self.assertEqual(expected_plex_stream.episode_number, output.episode_number)
            self.assertEqual(expected_plex_stream.episode_name, output.episode_name)
            self.assertEqual(expected_plex_stream.time_left, output.time_left)

            MockPlexServer.assert_called_once()
            self.assertEqual(2, mock_plex_server.sessions.call_count)
