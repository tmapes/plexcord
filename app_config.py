from dataclasses import dataclass


@dataclass
class AppConfig:
    """Class for configuring the service"""
    plex_server_address: str
    plex_user_token: str
    plex_username: str
    plex_poll_time: int
    discord_client_id: str
    discord_process_id: int

    def __init__(self,
                 plex_server_address: str,
                 plex_user_token: str,
                 plex_poll_time: int,
                 plex_username: str,
                 discord_client_id: str,
                 discord_process_id: int) -> None:
        self.plex_server_address = plex_server_address
        self.plex_user_token = plex_user_token
        self.plex_poll_time = plex_poll_time
        self.plex_username = plex_username
        self.discord_client_id = discord_client_id
        self.discord_process_id = discord_process_id
        super().__init__()
