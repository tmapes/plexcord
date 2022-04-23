from dataclasses import dataclass

import yaml


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

    @staticmethod
    def from_yaml_file(name: str) -> 'AppConfig':
        with open(name, 'r') as config:
            raw_config = yaml.load(config, Loader=yaml.FullLoader)
            parsed_config = AppConfig(
                plex_server_address=raw_config.get("plex", {}).get("server_address", "http://localhost:32400"),
                plex_user_token=raw_config.get("plex", {}).get("user_token", "aabbccdd"),
                plex_poll_time=raw_config.get("plex", {}).get("poll_time", 60),
                plex_username=raw_config.get("plex", {}).get("plex_username", ""),
                discord_client_id=raw_config.get("discord", {}).get("client_id", "aabbccdd"),
                discord_process_id=raw_config.get("discord", {}).get("process_id", 11223344),
            )
        return parsed_config
