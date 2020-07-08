from dataclasses import dataclass


@dataclass
class AppConfig:
    """Class for configuring the service"""
    plex_server_address: str
    plex_user_token: str
    discord_client_id: str
    discord_process_id: int

    def __init__(self, plex_server_address, plex_user_token, discord_client_id, discord_process_id) -> None:
        self.plex_server_address = plex_server_address
        self.plex_user_token = plex_user_token
        self.discord_client_id = discord_client_id
        self.discord_process_id = discord_process_id
        super().__init__()
